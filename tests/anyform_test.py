from tests import AnyFormTest
from flask_anyform import AForm

class BaseTests(AnyFormTest):
    def test_aform(self):
        self.assertIsNotNone(self.app.extensions['anyform'].provides['test'])
        self.assertEqual(self.app.extensions['anyform'].provides['test'].af_tag, 'test')
        self.assertIsInstance(self.app.extensions['anyform'].provides['test'], AForm)

    def test_extension(self):
        self.assertIsNotNone(self.app)
        self.assertIsNotNone(self.app.extensions['anyform'])
        self.assertEqual(self.app.extensions['anyform'], self.app.anyform_e)
        self.assertIsNotNone(self.app.extensions['anyform'].app)
        self.assertIsNotNone(self.app.extensions['anyform'].forms)
        self.assertIsNotNone(self.app.extensions['anyform'].provides)
        self.assertIsNotNone(self.app.extensions['anyform']._ctxs)

    def test_use(self):
        r = self._get('/')
        self.assertIn(b'value="TEST FORM"', r.data)
        self.assertNotIn(b'test2', r.data)
        self.assertIn(b"RETURNED FROM A FORM CONTEXT FUNCTION", r.data)
        self.assertNotIn(b"RETURNED FROM A TAGGED CONTEXT VALUE FUNCTION", r.data)
        r = self._get('/notindex')
        self.assertIn(b'value="TEST FORM TWO"', r.data)
        self.assertIn(b'test2', r.data)
        self.assertIn(b"RETURNED FROM A TAGGED CONTEXT VALUE FUNCTION", r.data)

if __name__ == '__main__':
    unittest.main()
