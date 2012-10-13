from flask_cloudfront.auth import CloudFrontRedirect
from base import BadRedirect, GoodRedirect, TestCase


class AuthTestCase(TestCase):
    def setUp(self):
        super(AuthTestCase, self).setUp()
        self.app = self.create_app()
        
    def test_no_location(self):
        self.assertRaises(KeyError, CloudFrontRedirect, None)

    def test_unauthorized(self):
        resp = BadRedirect('/', code=303, headers=None,
                           **self.app.config['CLOUDFRONT_CONFIG'])
        self.assertEqual(resp.go().status_code, 500)

    def test_authorized(self):
        resp = GoodRedirect('/', code=303, headers=None,
                            **self.app.config['CLOUDFRONT_CONFIG'])
        self.assertEqual(resp.go().status_code, 303)

