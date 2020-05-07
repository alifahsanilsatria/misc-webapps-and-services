from flask import Flask, request, render_template
from celery_example import make_celery

import requests, json, os, pika, sys, gzip, time

flask_app = Flask(__name__)
flask_app.config['SECRET_KEY'] = 'secret server 2'

UPLOAD_FOLDER = os.getcwd() + '/file_upload'
flask_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

celery_flask_app = make_celery(flask_app)

@flask_app.route('/', methods=['POST'])
def home():
    print("masuk server 2")
    if request.method == 'POST':
        file = request.files.get('file')
        x_routing_key = request.headers.get('X-ROUTING-KEY')

        file_path = os.path.join(flask_app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        json_resp = {"result" : "success"}

        compress_file.delay(file_path, x_routing_key)

        return json.dumps(json_resp)

@celery_flask_app.task(name='server2.compress_file')
def compress_file(file_path, x_routing_key):
    connection, channel = produce()

    file = open(file_path, 'r')

    stat_info = os.stat(file_path)
    file_size = stat_info.st_size

    progress = 0

    file_compress = gzip.open(os.getcwd() + '/file_compress/' + os.path.basename(file.name) + '.gz', 'wb')
    while progress < 1:
        content = file.read(int(0.1*file_size))
        file_compress.write(str.encode(content))
        progress += 0.1

        channel.basic_publish(exchange='1606882540',
                              routing_key=x_routing_key, 
                              body=str(progress*100) + '%')
        time.sleep(1)

def produce():
    credentials = pika.PlainCredentials('0806444524', '0806444524')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='152.118.148.95',
                                  port='5672',
                                  virtual_host='/0806444524',
                                  credentials=credentials
                                 ))
    channel = connection.channel()
    channel.exchange_declare(exchange='1606882540', exchange_type='direct')

    return connection, channel

if __name__ == '__main__':
    flask_app.run(debug=True, port=5000)