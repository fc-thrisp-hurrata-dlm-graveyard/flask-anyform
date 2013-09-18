from functools import partial
from collections import OrderedDict
from werkzeug.local import LocalProxy
from werkzeug.datastructures import MultiDict
from flask import request, current_app, get_template_attribute
from .utils import get_url


_anyform = LocalProxy(lambda: current_app.extensions['anyform'])
_endpoint = LocalProxy(lambda: request.endpoint.rsplit(':')[-1])
current_forms = LocalProxy(lambda: current_app.extensions['anyform'].get_current_forms)


class AForm(object):
    def __init__(self, **kwargs):
        self.af_tag = kwargs.get('af_tag')
        self.af_form = kwargs.get('af_form')
        self.af_template = kwargs.get('af_template')
        self.af_macro = kwargs.get('af_macro')
        self.af_points = self.set_points(kwargs.get('af_points'))

    def set_points(self, points):
        if points:
            return points
        else:
            return ['all']

    def update(self, **kwargs):
        [setattr(self, k, v) for k, v in kwargs.items()]

    @property
    def _renderable(self):
        return get_template_attribute(self.af_template, self.af_macro)

    @property
    def render(self):
        return self._renderable(self)

    #form in practice: set next, return with request.form if necessary
    #@property
    #def filled_form(self):
    #    if request.form:
    #        return self.af_form(request.form)

    def set_form_next(self, request):
        if getattr(self.af_form, 'next', None):
            self.af_form.next.data = get_url(request.args.get('next')) \
                or get_url(request.form.get('next')) or ''


class AnyForm(object):
    """
    The Flask-Anyform extension

    :param app: The application.
    :param forms: A list of AForm instances
    """
    def __init__(self,
                 app=None,
                 forms=None,
                 **kwargs):
        self.app = app
        self.forms = forms
        self._ctx_processors = {}

        if app is not None and forms is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Initializes the Flask-Anyform extension for the specified application.

        :param app: The application.
        :param forms: A list of AForm instances, or corresponding dicts
        """
        self.app = app

        self.set_provides(self.forms)

        self.register_context_processors(app, self._context_processors)

        app.extensions['anyform'] = self

    def set_provides(self, forms):
        setattr(self, 'provides', OrderedDict([self.init_provide(f) for f in forms]))

    def init_provide(self, f):
        if isinstance(f, dict):
            f = AForm(**f)
        return f.af_tag, f

    def register_context_processors(self, app, context_processors):
        app.jinja_env.globals.update(context_processors)

    @property
    def _context_processors(self):
        ctx_prc = {}
        for form in self.provides.values():
            ctx_prc.update(self.get_processor_for(form))
        ctx_prc.update({'anyform':_anyform, 'current_forms': current_forms})
        return ctx_prc

    def get_processor_for(self, form):
        return {"{}_form".format(form.af_tag): self.form_ctx_function(form)}

    def form_ctx_function(self, form):
        run_ctx = partial(self._run_form_ctx, form.af_tag)
        run_update = partial(form.update)
        return partial(self._on_form_ctx, form, run_ctx, run_update)

    def _on_form_ctx(self, form, run_ctx, run_update):
        run_update(**run_ctx())
        return form.render

    def _add_form_ctx(self, form, fn):
        group = self._ctx_processors.setdefault(form, [])
        fn not in group and group.append(fn)

    def _run_form_ctx(self, form):
        rv, fns = {}, []
        for g in [None, form]:
            for fn in self._ctx_processors.setdefault(g, []):
                rv.update(fn())
        return rv

    def form_ctx(self, fn):
        self._add_form_ctx(None, fn)

    def named_form_ctx(self, fn):
        fn_for_form = fn.__name__.rpartition('_')[0]
        self._add_form_ctx(fn_for_form, fn)

    @property
    def get_current_forms(self):
        return {k: v for k,v in self.provides.items() if self.form_in_endpoint(v.af_points)}

    def form_in_endpoint(self, vaf):
        return any([(v in [str(_endpoint), 'all']) for v in vaf])
