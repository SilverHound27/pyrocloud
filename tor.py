import threading
import time
import requests
import json
import subprocess

def torrent(port):
    command = subprocess.Popen(['qbittorrent-nox', f'--webui-port={port}'])

def ngrok(port, message):
    
    ngrok_cmd = subprocess.Popen(['ngrok', 'http', str(port)])    
    localhost_url = "http://localhost:4040/api/tunnels"

    time.sleep(1)
    tunnel_url = requests.get(localhost_url).text
    json_data = json.loads(tunnel_url)

    tunnel_url = json_data['tunnels'][0]['public_url']
    tunnel_url = tunnel_url.replace("https", "http")
    print('Running at localhost: ' + str(port))
    print(tunnel_url)
    message.reply_text('Running at localhost: ' + str(port) + "\n" + tunnel_url)

def start_tor(client, message):
    
    try:
        port = message.split()[-1]
    except:
        port = 9999

    thread_torrent = threading.Thread(target = torrent, args=(int(port),))
    thread_ngrok = threading.Thread(target = ngrok, args=(int(port), message))

    thread_torrent.start()
    print('Torrent server started!')

    time.sleep(5)
    print('Establishing secure connection!')
    
    thread_ngrok.start()
    print('Secure connection established...')
    print('Username: admin')
    print('password: adminadmin')
    
    thread_ngrok.join()
    thread_torrent.join()