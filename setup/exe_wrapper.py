import os
import sys
import threading
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

proc_lock = threading.Lock()
current_proc = None
t_libre = None

class Server(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return
    
    def do_GET(self):
        path = urlparse(self.path).path

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()

        match path:
            case '/start' | '/stop':
                response = 'you should use a POST request to start or stop the libretranslate server instead'
            case '/':
                response = 'hi'
            case '/favicon.ico':
                return
            case _:
                response = 'go away.'

        print(response)
        self.wfile.write(response.encode('UTF-8'))
        return

    def do_POST(self):
        path = urlparse(self.path).path

        match path:
            case '/start':
                parsed = urlparse(self.path)
                params = parse_qs(parsed.query)
                parsed_args = parse_args(params)

                global t_libre
                if not t_libre:
                    t_libre = threading.Thread(target=start_libre, args=(parsed_args,))

                if not t_libre.is_alive():
                    self.send_response(200)
                    response = 'Starting libretranslate thread'
                    t_libre.start()
                else:
                    self.send_response(418)
                    response = 'libretranslate thread is already running'
                
                self.send_header("Content-type", "text/plain")
                self.end_headers()

                print(response)
                self.wfile.write(response.encode('UTF-8'))
                return
        
            case '/stop':
                ok = stop_libre()
                self.send_response(200 if ok else 418)
                self.send_header("Content-type", "text/plain")
                self.end_headers()

                if ok:
                    response = 'Successfully terminated libretranslate process'
                else:
                    response = 'No libretranslate process running'

                print(response)
                self.wfile.write(response.encode('UTF-8'))
                return

            case _:
                self.send_response(418)
                self.send_header("Content-type", "text/plain")
                self.end_headers()

                response = 'Not a valid path'

                print(response)
                self.wfile.write(response.encode('UTF-8'))
                return

# http://127.0.0.1:2222
def start_listener():
    print('Listening on http://127.0.0.1:2222')
    HTTPServer(('127.0.0.1', 2222), Server).serve_forever()
    print('Listener closed')

# http://127.0.0.1:3333
def start_libre(args=["--load-only","en,de"]):
    global current_proc
    try:
        cmd = ["libretranslate", "--port", "3333"] + args
    except FileNotFoundError:
        print('libretranslate is not installed!')
    with proc_lock:
        if current_proc and current_proc.poll() is None:
            return
        current_proc = subprocess.Popen(cmd)
    try:
        current_proc.wait()
    finally:
        with proc_lock:
            current_proc = None

def stop_libre():
    global current_proc
    with proc_lock:
        p = current_proc
    if not p or p.poll() is not None:
        return False
    p.terminate()
    try:
        p.wait(5)
    except subprocess.TimeoutExpired:
        p.kill()
        p.wait()
    with proc_lock:
        current_proc = None
    global t_libre
    t_libre = None
    return True

def parse_args(args):
    parsed = []
    
    for k, v in args.items():
        parsed.append(f'--{k}')
        parsed.append(''.join(v))

    return parsed

def launch_game():
    try:
        args = sys.argv[1:]
        subprocess.Popen(
            [os.path.join(os.getcwd(), 'Titanfall2_real.exe'), *args],
            shell=False
        )
        return True
    except:
        print('Could not launch game!! Is this file in the correct directory? Did you rename the original .exe?')
        return False

def main():
    # if launch_game():
        threading.Thread(target=start_listener).start()
    
if __name__ == '__main__':
    main()

