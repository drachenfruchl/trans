import os
import sys
import threading
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer

class Server(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return
    def do_GET(self):
        html = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Trans</title>
            </head>
            <body>
        """

        if self.path == '/start':
            print('This would start a libretranslate server')
            self.send_response(200)

            html += """
                <h1>Hi twin</h1>
                <img src="https://media1.tenor.com/m/mY2LINXOxnQAAAAC/another-one-dj-khaled.gif" alt="" width="335" height="169">
            """
        else:
            print('This is not a valid path')
            self.send_response(404)
            
            html += """
                <h1>go away.</h1>
            """

        html += """
            </body>
            </html>
        """

        self.send_header("Content-type", "text/html")
        self.end_headers() 
        self.wfile.write(html.encode('UTF-8'))

def start_listener():
    HTTPServer(('127.0.0.1', 5001), Server).serve_forever()
threading.Thread(target=start_listener).start()

args = sys.argv[1:]

subprocess.Popen(
    [os.path.join(os.getcwd(), 'Titanfall2_real.exe'), *args],
    shell=False
)