"""
Flask-Anyform
------------

Flask application interface & integration of forms


Links
`````
* `documentation <http://packages.python.org/>`_
* `development version
  <http://github.com/thrisp/flask-anyfomr>`_

"""
from setuptools import setup

requires = ['Flask>=0.9']

setup(
    name='Flask-Anyform',
    version='0',
    url='http://',
    license='MIT',
    author='thrisp/hurrata',
    author_email='blueblank@gmail.com',
    description='Flask application form integration ',
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
