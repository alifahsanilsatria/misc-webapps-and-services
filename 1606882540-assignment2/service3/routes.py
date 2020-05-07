from service3 import app, db
from flask import request, send_file, redirect, url_for, send_from_directory, jsonify
from oauth import ambil_token, ambil_resource
import os
import datetime
from service3.models import FileMetadata

@app.route("/", methods=['POST'])
def create():
    uname = request.form.get('username')
    pw = request.form.get('password')
    client_id = request.form.get('client_id')
    client_secret = request.form.get('client_secret')

    resp = ambil_token(uname, pw, client_id, client_secret).json()
    if 'access_token' in resp:
        ## do something
        file = request.files['file_req']
        filename = file.filename
        file_size = len(file.read())
        file_date_time = datetime.datetime.now()

        file_metadata = FileMetadata(filename=filename, file_size = file_size, file_date_time = file_date_time)
        db.session.add(file_metadata)
        db.session.commit()

        return 'File metadata successfully saved'
        
    else:
        return '<h1>Wrong Credentials</h1>'

@app.route("/<id>", methods=["GET"])
def read(id):
    file_metadata = FileMetadata.query.filter_by(id=id).first()
    if file_metadata:
        return jsonify( id=id,
                        filename=file_metadata.filename,
                        file_size=file_metadata.file_size,
                        file_date_time=file_metadata.file_date_time)

    else:
        return "Not Found"

@app.route("/update/<id>", methods=["PATCH"])
def update(id):
    data = request.get_json()

    filtered_filemetadata = FileMetadata.query.filter_by(id=id)
    if filtered_filemetadata.count() > 0:
        filtered_filemetadata.update(data)
        db.session.commit()
        file_metadata_new = FileMetadata.query.filter_by(id=id).first()
        return jsonify(id=id,
                    filename=file_metadata_new.filename,
                    file_size=file_metadata_new.file_size,
                    file_date_time=file_metadata_new.file_date_time)
    else:
        return "Not Found"

@app.route("/delete/<id>", methods=["DELETE"])
def delete(id):
    filtered_filemetadata = FileMetadata.query.filter_by(id=id)
    if filtered_filemetadata.count() > 0:
        filtered_filemetadata.delete()
        db.session.commit()
        return "Deletion with id = " + id + " success"
    else:
        return "Not Found"