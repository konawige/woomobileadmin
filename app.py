from flask import Flask, url_for, request
from werkzeug.utils import redirect
from config import Config
from datetime import datetime
from flask import render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, StringField
from wtforms.validators import DataRequired
from urllib.parse import urlencode

import re
#import requests

app = Flask(__name__)
app.config.from_object(Config)

bootstrap = Bootstrap(app)

dev_environment = "TEST"


class AddForm(FlaskForm):
    auth_url = StringField(u'URL of your site', validators=[DataRequired()])
    user_id = StringField(u'Email address', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/auth', methods=['GET', 'POST'])
def home():
    form = AddForm()
    if form.validate_on_submit():
        store_url = 'https://' + form.auth_url.data
        endpoint = '/wc-auth/v1/authorize'
        if dev_environment == "TEST":
            start_return_url = "http://127.0.0.1:5000"
        else:
            start_return_url = "https://woomobileadmin.herokuapp.com"

        params = {
            "app_name": "Mobile Admin for Woocommerce",
            "scope": 'read_write',
            "user_id": "{}_site_{}".format(form.user_id.data, form.auth_url.data),
            "return_url": start_return_url + "/return-page",
            "callback_url": "https://us-central1-woo-mobile.cloudfunctions.net/postConsumerAuth"
        }
        query_string = urlencode(params)
        get_request = "%s%s?%s" % (store_url, endpoint, query_string)

        print(get_request)
        return redirect(get_request)
        

    return render_template("base_auth_reg.html", form=form)

@app.route('/return-page')
def return_after_auth():
    success = int(request.args.get('success'))
    user_id = request.args.get('user_id')
    if user_id is None:
        user_id = ''
    if success is None:
        success = 0

    return render_template("base_auth_result.html", success = success, user_id = user_id)
    


