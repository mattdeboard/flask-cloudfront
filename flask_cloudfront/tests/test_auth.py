from flask_cloudfront.auth import CloudFrontRedirect
from base import BadRedirect, GoodRedirect, TestCase


class AuthTestCase(TestCase):
    def test_no_location(self):
        self.assertRaises(KeyError, CloudFrontRedirect, None)
