from service1 import app
from flask import request
from flask import send_file
from oauth import ambil_token, ambil_resource
import gzip
import shutil
import os

@app.route("/", methods=['POST'])
def home():
    uname = request.form.get('username')
    pw = request.form.get('password')
    client_id = request.form.get('client_id')
    client_secret = request.form.get('client_secret')

    resp = ambil_token(uname, pw, client_id, client_secret).json()
    if 'access_token' in resp:
        ## do something
        file = request.files['file_req']

        with gzip.open(os.path.join(os.getcwd(), 'service1/compressed_files', file.filename + '.gz'), 'wb') as compressed_file:
            shutil.copyfileobj(file, compressed_file)
            return '<h1>Compression Success</h1>'
    else:
        return '<h1>Wrong Credentials</h1>'