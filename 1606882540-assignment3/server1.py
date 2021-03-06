from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit, send
from celery_example import make_celery
import requests, uuid, json, pika, time

server1_app = Flask(__name__)
server1_app.config['SECRET_KEY'] = 'secret server 1'
socketio = SocketIO(server1_app)

celery_flask_app = make_celery(server1_app)

@server1_app.route('/', methods=['GET','POST'])
def upload():
    if request.method == "POST":
        print("masuk server 1")

        file = request.files['file']
        unique_id = str(uuid.uuid4())

        consume.delay(unique_id)
        # do something
        r = requests.post('http://127.0.0.1:5000/',
                          files={ 'file' : file }, 
                          headers = {"X-ROUTING-KEY": unique_id})

        result = json.loads(r.text)

        return render_template('upload_result.html')
    else:
        return render_template('upload.html')

@celery_flask_app.task(name='server1.consume')
def consume(routing_key):
    credentials = pika.PlainCredentials('0806444524', '0806444524')
    connection = pika.BlockingConnection(
                    pika.ConnectionParameters(host='152.118.148.95',
                                            port='5672',
                                            virtual_host='/0806444524',
                                            credentials=credentials
                                            ))
    channel = connection.channel()

    channel.queue_declare(queue=routing_key, exclusive=True)
    channel.queue_bind(exchange='1606882540',
                       queue=routing_key,
                       routing_key=routing_key)

    channel.basic_consume(queue=routing_key, on_message_callback=receive_progress, auto_ack=True)
    print(' [*] Waiting for messages')

    channel.start_consuming()

def receive_progress(ch, method, properties, body): 
    print("masuk receive progress")

    print(" [x] %r" % body)

@socketio.on('display_progress')
def display_progress(json):
    print('received json: ' + str(json))
    emit('display_progress', 10, broadcast=True)

@socketio.on('upgrade_progress')
def upgrade_progress(progress):
    time.sleep(1)
    emit("display_progress", progress);

if __name__ == '__main__':
    socketio.run(server1_app, debug=True, port=15674)