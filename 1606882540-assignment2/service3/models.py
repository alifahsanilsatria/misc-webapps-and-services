from service3 import db

class FileMetadata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(80), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    file_date_time = db.Column(db.String(80), nullable=False)

