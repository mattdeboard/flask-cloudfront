================
Flask-CloudFront
================

A library for providing an authorization layer between a user's browser and your sensitive data being served by Amazon's CloudFront service.

About
=====

This project was born out of a need I had for a lightweight authorization server that could sit between a CloudFront distribution and the `Courseload <http://courseload.com>`_ API client. It is an expression of a strategy leveraging CloudFront's `signed URL <http://docs.amazonwebservices.com/AmazonCloudFront/latest/DeveloperGuide/PrivateContent.html>`_ feature for serving private content combined with an authorize-every-request constraint. I could not find any good front-to-back solutions out there so I made one myself.

Usage
=====

The API is provided by ``flask_cloudfiles.auth.CloudFilesRedirect``. You will need to create a subclass and override the ``authorize`` method with your own authorization logic. That method should return an integer correlated with an HTTP response code, e.g. 200, 204, 404, 500, etc. Example::

  from flask.ext.cloudfiles import CloudFilesRedirect


  class MyRedirect(CloudFilesRedirect):
      def authorize(self, *args):
          result = do_some_stuff(*args)
          if result:
              return 200
          return 404

You can then call the class instance's ``go`` method to perform the authorization, cryptographic signing & signed URL generation. If you return the value of that method invocation, the user will be redirected to the location you specify::

  @app.route('/')
  def home():
      my_redirect = MyRedirect(app.config['CLOUDFRONT_DOMAIN'], code=303, headers={},
                               **app.config['CLOUDFRONT_CONFIG'])
      return my_redirect.go()

HTTP 303
--------

I chose to make HTTP 303 the default redirect code because by default and by specification HTTP 303 is not cached by browsers. Because the signed URLs are time-bound, caching the redirect could have disasterous results on user experience (i.e. hitting a cached redirect for an expired link == 404). However you can pass whatever code you like when you instantiate your class.

Configuration
=============

There is one recommended configuration setting and one mandatory.

Mandatory: ``CLOUDFRONT_CONFIG``. This is a dictionary in the following format::

  CLOUDFRONT_CONFIG = {
    'priv_key_string': '/path/to/pk-ABCDEF.pem',
    'key_pair_id': 'ABCDEF',
    # How many seconds from the time the signature is generated it will expire.
    # Keys generated using a value of 60 for this key will expire one minute
    # after they are created
    'expires': 60
  }

Recommended: ``CLOUDFRONT_DOMAIN``. This is a string that refers to the domain or CNAME of your CloudFront distribution, e.g. ``http://dc1097jtk.cloudfront.net``.



   

