from flask import Flask, render_template, session, request, redirect, url_for
import requests
import os
import re
import models
import json

config = json.load(open('config.json'))

app = Flask(__name__)
app.secret_key = config['secret']
AUTOCERT_PATH = config['path']

def add_domain(domain):
    out = os.popen("cd %s; sudo python3 domain.py %s" % (AUTOCERT_PATH, domain)).read()
    return out.split('\n')

@app.route('/', methods=['POST','GET'])
def login():
    error = ''
    if request.method == 'POST':
        log = models.verify(request.form['username'], request.form['password'])
        if log:
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        error = 'Username or password incorrect.'
    return render_template('login.html', error=error)

@app.route('/main', methods=['POST','GET'])
def index():
    output = ''
    if not 'username' in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        domain = request.form['domain']
        output = add_domain(domain)
    domains = []
    for file in os.listdir("/etc/nginx/sites-available"):
        if file.endswith(".conf"):
            domains.append(file[:-5])
    return render_template('index.html', domains=domains, output=output, error=False)

@app.route('/update', methods=['POST'])
def update():
    if request.form['password1'] != request.form['password2']:
        return render_template('index.html', error=True, errorText="Passwords must match")
    models.changePass(session['username'], request.form['password1'])
    return render_template('index.html', error=False)

if __name__ == '__main__':
    app.run()
