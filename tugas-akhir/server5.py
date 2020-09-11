from flask import Flask, render_template, request, redirect, url_for
import uuid, json, pika, time, threading, ntpath, os, requests, ntpath, time

app = Flask(__name__)

def initiate_rabbitmq():
    credentials = pika.PlainCredentials('0806444524', '0806444524')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='152.118.148.95',
                                  port='5672',
                                  virtual_host='/0806444524',
                                  credentials=credentials
                                 ))
    channel = connection.channel()
    
    channel.exchange_declare(exchange='1606882540_TOPIC', exchange_type='topic')

    resulting_queue = channel.queue_declare(queue='')
    queue_name = resulting_queue.method.queue
    channel.queue_bind(exchange='1606882540_TOPIC',
                       queue=queue_name,
                       routing_key='server')

    while True:
        live_time = json.dumps({'server5' : str(int(time.time()))})
        channel.basic_publish(exchange='1606882540_TOPIC',
                            routing_key='server',
                            body=live_time)
        # print(live_time)
        time.sleep(1)

if __name__ == '__main__':
    t = threading.Thread(target=initiate_rabbitmq)
    t.start()

    app.run(debug=True, port=5005)