"""
Flask-Anyform
------------

Flask application meta-form integration


Links
`````
* `documentation <http://packages.python.org/>`_
* `development version
  <http://github.com/thrisp/flask-anyform>`_

"""
from setuptools import setup

requires = ['Flask>=0.9']

setup(
    name='Flask-Anyform',
    version='0.0.4',
    url='http://github.com/thrisp/flask-anyform',
    license='MIT',
    author='thrisp/hurrata',
    author_email='blueblank@gmail.com',
    description='Flask application for form integration ',
    long_description=__doc__,
    packages=['flask_anyform'],
    test_suite="test",
    zip_safe=False,
    platforms='any',
    install_requires=requires,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
