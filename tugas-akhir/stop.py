import subprocess

subprocess.run('sudo kill -9 `sudo lsof -t -i:5001` & ' +
               'sudo kill -9 `sudo lsof -t -i:5002` & ' +
               'sudo kill -9 `sudo lsof -t -i:5003` & ' +
               'sudo kill -9 `sudo lsof -t -i:5005` & ' +
               'sudo service nginx stop &', shell=True)