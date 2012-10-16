from flask import current_app, make_response, redirect, Response

from cloudfront_sign import get_canned_policy_url


class CloudFrontRedirect(object):
    def __init__(self, location='', code=303, headers=None, **cf_config):
        if not location:
            try:
                self.location = current_app.config['CLOUDFRONT_DOMAIN']
            except KeyError:
                raise KeyError("You must either set the 'CLOUDFRONT_DOMAIN' "
                               "constant or provide a value for the 'location' "
                               "param.")

        if isinstance(location, unicode):
            # If the URL string is unicode, there seems to be a misfire between
            # the digital signing of the policy and the URL as entered into the
            # bar, at least in Chrome 22.0.1229.79.
            location = str(location)

        self.location = location
        signed_url = get_canned_policy_url(self.location, **cf_config)
        resp = make_response(redirect(signed_url, code))
        self.redirect = self.headers(resp, headers or {})

    def headers(self, resp, headers):
        for header, value in headers.items():
            resp[header] = value

        return resp

    def authorize(self, *args, **kwargs):
        """Override this method with your own authorization logic."""
        raise NotImplementedError

    def go(self, good_codes=None, bad_codes=None, *args, **kwargs):
        good_codes = good_codes or [200, 204]
        auth_status = self.authorize(*args, **kwargs)

        if int(auth_status) in good_codes:
            return self.redirect

        return Response(status=auth_status)

