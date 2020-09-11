from flask import Flask, render_template, request, redirect, url_for
import uuid, json, pika, time, threading, ntpath, os, requests, ntpath

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        url_list = request.form.getlist('url')
        routing_key = str(uuid.uuid4())
        # t = threading.Thread(target=create_url_sender, args=(url_list,))
        # t.start()
        initiate_connection_from_server2(routing_key)

        t = threading.Thread(target=publish_url_list_from_server1, args=(url_list, routing_key))
        t.start()

        return render_template('client.html', url_list=url_list)

def publish_url_list_from_server1(url_list, routing_key):
    credentials = pika.PlainCredentials('0806444524', '0806444524')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='152.118.148.95',
                                  port='5672',
                                  virtual_host='/0806444524',
                                  credentials=credentials
                                 ))
    channel = connection.channel()

    # print('masuk basic publish di server1')
    # print(';'.join(url_list))
    channel.basic_publish(exchange='1606882540_DIRECT',
                            routing_key=routing_key,
                            body=';'.join(url_list))
    connection.close()

def initiate_connection_from_server2(routing_key):
    payload = {'routing_key' : routing_key}
    # headers = {'Content-Type': 'application/json'}

    requests.post('http://127.0.0.1:5002', json=payload)
    time.sleep(1)

if __name__ == '__main__':
    app.run(debug=True, port=5001)