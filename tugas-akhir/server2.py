from flask import Flask, render_template, request, redirect, url_for
import uuid, json, pika, time, threading, ntpath, os, requests, ntpath

app = Flask(__name__)

routing_key = None

@app.route('/', methods=['POST'])
def index():
    global routing_key
    payload = request.get_json(force=True)
    routing_key = payload['routing_key']
    t = threading.Thread(target=create_url_receiver, args=(routing_key,))
    t.start()

    return '200'

def callback(ch, method, properties, body):
    global routing_key
    url_list = body.decode("utf-8").split(';')
    thread_list = []
    for idx_url, url in enumerate(url_list):
        url_number = idx_url+1
        t = threading.Thread(target=download_file, args=(url, url_number, routing_key))
        t.start()
        thread_list.append(t)

    for t in thread_list:
        t.join()

    payload = {'routing_key' : routing_key}
    requests.post('http://127.0.0.1:5003', json=payload)

def download_file(url, url_number, routing_key):
    # print(url)
    credentials = pika.PlainCredentials('0806444524', '0806444524')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='152.118.148.95',
                                  port='5672',
                                  virtual_host='/0806444524',
                                  credentials=credentials
                                 ))
    channel = connection.channel()

    r = requests.get(url, stream=True)
    content_length = int(r.headers['content-length'])
    # print("File length:")
    # print(content_length)
    download_folder = os.getcwd() + '/static/downloads/' +  routing_key

    try:
        os.mkdir(download_folder)
    except:
        pass

    file_name = ntpath.basename(url)
    file_path = os.path.join(download_folder, file_name)
    with open(file_path, 'wb') as fd:
        dl = 0
        for chunk in r.iter_content(chunk_size=int(content_length/10)):
            fd.write(chunk)
            dl += len(chunk)
            percentage = 100 * (dl / content_length)

            channel.exchange_declare(exchange='1606882540_TOPIC', exchange_type='topic')

            progress_info = json.dumps({'server2' : str(url_number) + '-' + str(percentage) + '%'})

            channel.basic_publish(exchange='1606882540_TOPIC',
                            routing_key='server',
                            body=progress_info)
            time.sleep(0.1)

def create_url_receiver(routing_key):
    credentials = pika.PlainCredentials('0806444524', '0806444524')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='152.118.148.95',
                                  port='5672',
                                  virtual_host='/0806444524',
                                  credentials=credentials
                                 ))
    channel = connection.channel()
    channel.exchange_declare(exchange='1606882540_DIRECT', exchange_type='direct')

    resulting_queue = channel.queue_declare(queue='')
    queue_name = resulting_queue.method.queue

    channel.queue_bind(exchange='1606882540_DIRECT',
                       queue=queue_name,
                       routing_key=routing_key)
    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

if __name__ == '__main__':
    app.run(debug=True, port=5002)