
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import pymysql


# Database connection settings are provided through environment variables.
DB_HOST = os.environ["DB_HOST"]
DB_NAME = os.environ["DB_NAME"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]


def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        connect_timeout=5,
        cursorclass=pymysql.cursors.DictCursor
    )


def initialize_database():
    # Create the messages table if it does not already exist.
    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    message VARCHAR(500) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        connection.commit()
    finally:
        connection.close()


class ApplicationHandler(BaseHTTPRequestHandler):

    def send_json(self, status_code, response):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response, default=str).encode())

    def do_GET(self):
        try:
            if self.path == "/health":
                connection = get_db_connection()
                connection.close()

                self.send_json(200, {
                    "status": "healthy",
                    "database": "connected"
                })

            elif self.path == "/" or self.path == "/messages":
                connection = get_db_connection()

                try:
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "SELECT id, message, created_at "
                            "FROM messages ORDER BY id DESC LIMIT 50"
                        )
                        messages = cursor.fetchall()
                finally:
                    connection.close()

                self.send_json(200, {
                    "application": "Three-Tier Demo",
                    "messages": messages
                })

            else:
                self.send_json(404, {"error": "Not Found"})

        except Exception:
            self.send_json(503, {
                "error": "Application or database unavailable"
            })

    def do_POST(self):
        if self.path != "/message":
            self.send_json(404, {"error": "Not Found"})
            return

        try:
            content_length = int(self.headers.get("Content-Length", 0))

            if content_length <= 0 or content_length > 10000:
                self.send_json(400, {"error": "Invalid request size"})
                return

            data = json.loads(self.rfile.read(content_length))
            message = data.get("message", "").strip()

            if not message or len(message) > 500:
                self.send_json(400, {
                    "error": "Message must contain 1 to 500 characters"
                })
                return

            connection = get_db_connection()

            try:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO messages (message) VALUES (%s)",
                        (message,)
                    )
                    message_id = cursor.lastrowid

                connection.commit()
            finally:
                connection.close()

            self.send_json(201, {
                "status": "saved",
                "id": message_id,
                "message": message
            })

        except (ValueError, json.JSONDecodeError):
            self.send_json(400, {"error": "Invalid JSON"})
        except Exception:
            self.send_json(503, {
                "error": "Application or database unavailable"
            })


# Create the database table before accepting HTTP requests.
initialize_database()

server = HTTPServer(("0.0.0.0", 5000), ApplicationHandler)

print("Application server is running on port 5000")

server.serve_forever()
