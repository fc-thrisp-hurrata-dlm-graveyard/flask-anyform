from functools import partial
from collections import OrderedDict
from werkzeug.local import LocalProxy
from werkzeug.datastructures import MultiDict
from flask import request, current_app, get_template_attribute
from .utils import get_url


_anyform = LocalProxy(lambda: current_app.extensions['anyform'])
_endpoints = LocalProxy(lambda: [str(x) for x in (request.endpoint.rsplit(':')[-1],
                                                  request.endpoint.rsplit('.')[-1],
                                                  u'all')])
current_forms = LocalProxy(lambda: current_app.extensions['anyform'].get_current_forms())


def endpoints_list(request):
    [str(x) for x in (request.endpoint.rsplit(':')[-1],
                      request.endpoint.rsplit('.')[-1],
                      u'all')]

class AForm(object):
    def __init__(self, **kwargs):
        self.af_tag = kwargs.get('af_tag')
        self.af_form = kwargs.get('af_form')
        self.af_template = kwargs.get('af_template')
        self.af_view_template = kwargs.get('af_view_template')
        self.af_macro = kwargs.get('af_macro')
        self.af_points = self.set_points(kwargs.get('af_points'))
        self.populate = kwargs.get('populate', True)

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

    def render(self):
        return self._renderable(self)

    @property
    def form(self):
        if request.form:
            f = self.af_form(request.form)
            f.validate()
        elif request.json:
            f = self.af_form(MultiDict(request.json))
            f.validate()
        else:
            f = self.af_form()
        self.set_form_next(f)
        return f

    def set_form_next(self, form):
        if getattr(form, 'next', None):
            form.next.data = get_url(request.args.get('next')) \
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
        self._ctxs = {}
        self._ctx_prc = {}

        if app is not None and forms is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Initializes the Flask-Anyform extension for the specified application.

        :param app: The application.
        :param forms: A list of AForm instances, or corresponding dicts
        """
        self.app = app

        self.init_provides(self.forms)

        self.register_context_processors(app, self.init_context_processors())

        app.extensions['anyform'] = self

    def init_provides(self, forms):
        setattr(self, 'provides', OrderedDict([self.init_provide(f) for f in forms]))

    def init_provide(self, f):
        if isinstance(f, dict):
            f = AForm(**f)
        return f.af_tag, f

    def register_context_processors(self, app, context_processors):
        app.jinja_env.globals.update(context_processors)

    def init_context_processors(self):
        for form in self.provides.values():
            self._ctx_prc.update(self.get_processor_for(form))
        self._ctx_prc.update({'anyform':_anyform, 'current_forms': current_forms})
        return self._ctx_prc

    def get_processor_for(self, form):
        return {"{}_form".format(form.af_tag): self.form_ctx_function(form)}

    def form_ctx_function(self, form):
        run_ctx = partial(self._run_form_ctx, form.af_tag)
        run_update = partial(form.update)
        return partial(self._on_form_ctx, form, run_ctx, run_update)

    def _on_form_ctx(self, form, run_ctx, run_update):
        run_update(**run_ctx())
        return form.render()

    def _add_form_ctx(self, tag, fn):
        group = self._ctxs.setdefault(tag, [])
        fn not in group and group.append(fn)

    def _run_form_ctx(self, tag):
        rv, fns = {}, []
        for g in [None, tag]:
            for fn in self._ctxs.setdefault(g, []):
                rv.update(fn())
        return rv

    def init_fn_name(self, name):
        if name.partition('_')[0] == 'anyform':
            return None
        else:
            return name.rpartition('_')[0]

    def form_ctx(self, fn):
        """add a function to inject ctx into aforms at render
        To add context to all aforms name your function starting
        with 'anyform':

            @anyform.form_ctx
            def anyform_dostuff_ctx_fn():
               do stuff

        to add a function to a specific aform start with the aform tag:

            @anyform.form_ctx
            def myform_ctx():
                do stuff
        """
        self._add_form_ctx(self.init_fn_name(fn.__name__), fn)

    def get_current_forms(self):
        return {k: v for k,v in self.provides.items() if self.form_in_endpoint(v.af_points)}

    def form_in_endpoint(self, af_points):
        return any([(x in _endpoints) for x in af_points])
