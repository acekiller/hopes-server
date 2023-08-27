from create_app import App
import controllers as _
import api as _
from flask import request, render_template

from app_tools import AuthException, refreshTokenIfNeed

app = App.create_app()

@app.before_request
def before_request():
    pass

@app.errorhandler(AuthException)
def unauthorized(error):
    return render_template("401.html")

@app.after_request
def after_request(response):
    if (response.status_code == 200):
        refreshTokenIfNeed(response)
    return response

