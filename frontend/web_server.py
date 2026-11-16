import http.server
import socketserver

IP = ""
PORT = X

handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer((IP , PORT) , handler) as web_server:
    print(f"Serving at : ({IP}:{PORT})")
    web_server.serve_forever()