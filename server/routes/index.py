from server import app
from flask import render_template, redirect, url_for

@app.route('/')
def hello_world():
    # return app.send_static_file('index.html')
    return redirect(url_for('explorer'))

@app.errorhandler(404)
@app.route("/error404")
def page_not_found(error):
    return app.send_static_file('404.html')

@app.errorhandler(500)
@app.route("/error500")
def requests_error(error):
    return app.send_static_file('500.html')
