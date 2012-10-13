from flask import Flask
from flask_cloudfront.auth import CloudFrontRedirect
from flask.ext.testing import TestCase as _TestCase
import test_settings

class GoodRedirect(CloudFrontRedirect):
    def authorize(self):
        return 200


class BadRedirect(CloudFrontRedirect):
    def authorize(self):
        return 500
        
    
class TestCase(_TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.secret_key = 'secret'
        app.config.from_object(test_settings)
        return app

