from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class ApplicationHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            response = {
                "application": "Three-Tier Demo",
                "message": "Hello from the Application Tier!"
            }
            self.send_response(200)

        elif self.path == "/health":
            response = {
                "status": "healthy"
            }
            self.send_response(200)

        else:
            response = {
                "error": "Not Found"
            }
            self.send_response(404)

        self.send_header("Content-Type", "application/json")
        self.end_headers()

        self.wfile.write(json.dumps(response).encode())


server = HTTPServer(("0.0.0.0", 5000), ApplicationHandler)

print("Application server is running on port 5000")

server.serve_forever()