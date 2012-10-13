"""
Flask-CloudFront
----------------

A library for serving data from S3 buckets via CloudFront.

"""
from setuptools import setup

setup(
    name='Flask-CloudFront',
    version='0.1',
    license='BSD',
    author='Matt DeBoard',
    author_email='matt.deboard@gmail.com',
    description='Serve data securely from CloudFront.',
    long_description=__doc__,
    py_modules=['flask_cloudfront'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'Flask-Testing',
        'requests'
    ],
    tests_require='nose',
    test_suite='nose.collector',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
