flask-anyform
----

Form management for flask applications.

Created as natural progression on work done with [flask-security inline_forms branch](https://github.com/thrisp/flask-security)
 & [flack](https://github.com/thrisp/flack), this extension abstracts common
form integration tasks for flask applications.

example: 

    from flask import Flask
    from flask_anyform import AnyFrom, AForm
    from my_forms import MyForm

    app = Flask(__name__)

    my_aform = AForm(af_tag='my',
                     af_form=MyForm,
                     af_template='my_form.html',
                     af_macro='my_form_macro')

    AnyForm(app=app, forms=[my_aform])


Now render your (context & request aware) form anywhere with the specified macro
in the specified tempalte using 'my_form()'. Update and handle your form in controllers
and views only where you explicitly need to.

Work in progress
