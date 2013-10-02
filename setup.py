"""
Flask-Anyform
-------------

Flask application & extension form integration


Links
`````
* `documentation <http://pythonhosted.org/Flask-Anyform>`_
* `development version <http://github.com/thrisp/flask-anyform>`_

"""
from setuptools import setup

requires = ['Flask>=0.10']

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
    zip_safe=False,
    platforms='any',
    install_requires=requires,
    test_suite='nose.collector',
    tests_require=[
        'nose',
        'flask-wtf'
        'wtforms'
    ],
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
