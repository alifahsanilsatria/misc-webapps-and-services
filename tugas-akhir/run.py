import subprocess

subprocess.run('python3 server1.py & ' +
               'python3 server2.py & ' + 
               'sudo python3 server3.py & ' +
               'python3 server5.py & ' +
               'sudo service nginx start &', shell=True)