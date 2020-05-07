from service2 import app
from flask import request, send_file, redirect, url_for, send_from_directory
from oauth import ambil_token, ambil_resource
import os

@app.route("/", methods=['POST'])
def upload_file():
    uname = request.form.get('username')
    pw = request.form.get('password')
    client_id = request.form.get('client_id')
    client_secret = request.form.get('client_secret')

    resp = ambil_token(uname, pw, client_id, client_secret).json()
    if 'access_token' in resp:
        ## do something
        file = request.files['file_req']
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return redirect(url_for('uploaded_file',
                                    filename=file.filename))
        
    else:
        return '<h1>Wrong Credentials</h1>'

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return request.base_url + "/download"

@app.route('/uploads/<filename>/download')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)