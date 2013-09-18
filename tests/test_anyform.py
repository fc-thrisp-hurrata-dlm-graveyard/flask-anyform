from __future__ import with_statement
import hmac
import unittest
from flask_anyform import AnyForm, AForm
from test_app import create_app

class AnyFormTest(unittest.TestCase):
    def setUp(self):
        super(AnyFormTest, self).setUp()

        app_kwargs = self.APP_KWARGS
        app = self._create_app(self.ANYFORM_CONFIG or {}, **app_kwargs)
        app.debug = False
        app.config['TESTING'] = True

        app.anyform_e = AnyForm(app, forms=[])

        self.app = app
        self.client = app.test_client()

        with self.client.session_transaction() as session:
            session['csrf'] = 'csrf_token'

        csrf_hmac = hmac.new(self.app.config['SECRET_KEY'],
                             'csrf_token'.encode('utf8'), digestmod=sha1)
        self.csrf_token = '##' + csrf_hmac.hexdigest()

    def _create_app(self, anyform_config, **kwargs):
        return create_app(anyform_config, **kwargs)

    def _get(self,
             route,
             content_type=None,
             follow_redirects=None,
             headers=None):
        return self.client.get(route,
                               follow_redirects=follow_redirects,
                               content_type=content_type or 'text/html',
                               headers=headers)

    def _post(self,
              route,
              data=None,
              content_type=None,
              follow_redirects=True,
              headers=None):
        if isinstance(data, dict):
            data['csrf_token'] = self.csrf_token

        return self.client.post(route,
                                data=data,
                                follow_redirects=follow_redirects,
                                content_type=content_type or
                                'application/x-www-form-urlencoded',
                                headers=headers)


if __name__ == '__main__':
    unittest.main()
