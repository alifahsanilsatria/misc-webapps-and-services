from flask import Flask, render_template, request, redirect, url_for
import uuid, json, pika, time, threading, ntpath, os, urllib.request, requests, ntpath

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('client.html')
    else:
        connection, channel = produce()

        url = request.form['url']
        file_name = ntpath.basename(url)

        t = threading.Thread(target=download, args=(url, connection, channel, file_name))
        t.start()

        return render_template('client.html')

def download(url, connection, channel, file_name):
    req = urllib.request.Request(url, method='HEAD')
    response = urllib.request.urlopen(req)
    total_length = int(response.headers['Content-Length'])

    response = requests.get(url, stream=True)

    download_folder = os.getcwd() + '/static/downloads'
    file_path = os.path.join(download_folder, file_name)
    f = open(file_path, 'wb')

    dl = 0
    for data in response.iter_content(chunk_size=1024):
        dl += len(data)
        f.write(data)
        percentage = 100 * (dl / total_length)
        channel.basic_publish(exchange='1606882540',
                            routing_key='fffff',
                            body=str(percentage) + '%')
        if percentage == 100.0:
            channel.basic_publish(exchange='1606882540',
                            routing_key='fffff',
                            body='http://127.0.0.1:5000/static/downloads/' + file_name)


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

    channel.queue_declare(queue='fffff')
    channel.queue_bind(exchange='1606882540',
                       queue='fffff',
                       routing_key='fffff')

    return connection, channel

if __name__ == '__main__':
    app.run(debug=True, port=5000)