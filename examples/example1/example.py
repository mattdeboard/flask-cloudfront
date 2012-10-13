import urlparse

import requests
from flask import Flask
from flask.ext.cloudfront import CloudFrontRedirect

import settings

app = Flask(__name__)
app.config.from_object('settings')
cache = app.config['CACHE']


class MyCloudFrontRedirect(CloudFrontRedirect):
    def authorize(self, slug):
        sessionid = request.cookies.get('sessionid', '').strip()

        if not sessionid:
            return 401

        cache_key = '%s::%s' % (sessionid, slug)
        status = 200
        
        if not cache.get(cache_key):
            status = self._validate(sessionid, slug)
            if status == 200:
                cache.set(cache_key, 300)

        return status

    def _validate(self, sessionid, slug):
        url = urlparse.urljoin(request.host, 'api/v1/content/auth/%s' % slug)
        resp = requests.get(url, cookies={'sessionid': sessionid})
        return resp.status_code

@app.route('/content/<path:resource>/', methods=['GET'])
def content(resource):
    # URLs look like '/content/some-book-slug/page/1'
    slug, rest = resource.split('/', 1)
    headers = {
        'Cache-Control': 'public',
        'Content-Type': 'application/json'
    }
    cf_redirect = MyCloudFrontRedirect(headers=headers,
                                       **app.config['CLOUDFRONT_CONFIG'])
    return cf_redirect.go(slug=slug)

