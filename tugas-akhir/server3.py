from flask import Flask, render_template, request, redirect, url_for
import uuid, json, pika, time, threading, ntpath, os, requests, ntpath, gzip, shutil, subprocess, zipfile

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():    
    payload = request.get_json(force=True)
    routing_key = payload['routing_key']
    # print(routing_key)
    t = threading.Thread(target=compress_file_and_generate_secured_link, args=(routing_key,))
    t.start()

    return '200'

def compress_file_and_generate_secured_link(routing_key):
    credentials = pika.PlainCredentials('0806444524', '0806444524')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='152.118.148.95',
                                  port='5672',
                                  virtual_host='/0806444524',
                                  credentials=credentials,
                                 ))
    channel = connection.channel()

    dirs_src = os.listdir(os.getcwd() + '/static/downloads/' + routing_key)
    dirs_dest = os.getcwd() + '/static/downloads/' + routing_key + '.zip'
    total_files = len(dirs_src)

    # writing files to a zipfile
    zip_file = zipfile.ZipFile(dirs_dest, 'w')
    with zip_file:
        # writing each file one by one
        for idx_dir, dir_ in enumerate(dirs_src):
            zip_file.write('./static/downloads/' + routing_key + '/' + dir_)
            
            percentage = 100 * (idx_dir+1) / total_files
            progress_info = json.dumps({'server3' : str(percentage) + '%'})
            # print(progress_info)
            channel.basic_publish(exchange='1606882540_TOPIC',
                            routing_key='server',
                            body=progress_info)
            time.sleep(1)

    cmd = 'mv {src} {dest}'.format(src=dirs_dest, dest= '/usr/share/nginx/html/nginx-files/' + routing_key + '.zip')
    subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()

    cmd = 'rm -rf {src}'.format(src=os.getcwd() + '/static/downloads/' + routing_key)
    subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()

    secret_param = 'enigma'
    cmd = "echo -n '{routing_key}.zip{secret_param}' | md5sum ".format(routing_key=routing_key, secret_param=secret_param)
    cmd += "| awk '{print $1}'"
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    md5 = output.decode('utf-8').rstrip()
    
    secured_link = 'http://127.0.0.1:5004/file/{md5}/{routing_key}.zip'.format(md5=md5, routing_key=routing_key)
    secured_link_info = json.dumps({'server3-link' : secured_link})
    
    # print(secured_link)
    # print(secured_link_info)
    channel.basic_publish(exchange='1606882540_TOPIC',
                          routing_key='server',
                          body=secured_link_info)
    connection.close()

if __name__ == '__main__':
    app.run(debug=True, port=5003)