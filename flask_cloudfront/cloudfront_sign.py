# Code in this module adapted from a StackOverflow answer by user secretmike:
# http://stackoverflow.com/a/6624431

import base64
import time
import urlparse
from urllib import urlencode
from M2Crypto import EVP

def _aws_url_base64_encode(msg):
    msg_base64 = base64.b64encode(msg)
    msg_base64 = msg_base64.replace('+', '-')
    msg_base64 = msg_base64.replace('=', '_')
    msg_base64 = msg_base64.replace('/', '~')
    return msg_base64

def _sign_string(message, priv_key_string):
    key = EVP.load_key_string(priv_key_string)
    key.reset_context(md='sha1')
    key.sign_init()
    key.sign_update(message)
    signature = key.sign_final()
    return signature

def _create_url(url, encoded_signature, key_pair_id, expires):
    params = {
        'Expires': expires,
        'Signature': encoded_signature,
        'Key-Pair-Id': key_pair_id
    }
    # Coerce our URL into a ParseResult namedtuple.
    url = list(urlparse(url))
    # Using this clunky-looking way because the 'parse_qs' method returns a
    # a dict that doesn't URL encode well.
    query = dict(urlparse.parse_qsl(url.query))
    # Add our new signed URL parameters to any existing query params that may
    # have come in the original request.
    query.update(params)
    query = urlencode(query)
    url[4] = query
    return urlparse.urlunparse(url)

def get_canned_policy_url(url, priv_key_string, key_pair_id, expires):
    """
    Generate a signed CloudFront URL. Ref: http://goo.gl/8LEUI

    :type url: string
    :param url: Absolute URL for a resource hosted on S3 and served by
    CloudFront.
    
    :type priv_key_string: string
    :param priv_key_string: Path to the CloudFront private key file,
    a .pem file.
    
    :type key_pair_id: string
    :param key_pair_id: The ID the key pair. This is provided by AWS and
    is in the .pem filename, i.e. pk-<key_pair_id>.pem.
    
    :type expires: integer
    :param expires: Time in seconds for how long from "now" this URL
    should expire.

    :rtype: :class: `str`
    :return: The `url` param with authentication & authorization URL
    parameters appended.
    
    """
    expires = int(time.time()) + 300
    # We manually construct this policy string to ensure formatting matches
    # signature.
    canned_policy = ('{"Statement":[{"Resource":"%(url)s","Condition":'
                     '{"DateLessThan":{"AWS:EpochTime":%(expires)s}}}]}' %
                     {'url':url, 'expires':expires})
    # Sign the non-encoded policy
    signature = _sign_string(canned_policy, open(priv_key_string).read())
    # Now base64 encode the signature (URL safe as well)
    encoded_signature = _aws_url_base64_encode(signature)
    signed_url = _create_url(url, encoded_signature, key_pair_id, expires);
    return signed_url

