from flask import Flask
import os

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'service2/uploaded_files')

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba246'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER