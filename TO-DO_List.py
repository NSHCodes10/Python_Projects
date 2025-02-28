import json
import mysql.connector
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

# Database connection
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="your_user",
        password="your_password",
        database="todo_db"
    )

# HTTP Request Handler
class TodoHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

    def do_GET(self):
        """ Handle GET request to fetch all tasks """
        if self.path == "/tasks":
            conn = connect_db()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM tasks")
            tasks = cursor.fetchall()
            conn.close()
            
            self._set_headers()
            self.wfile.write(json.dumps(tasks).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not Found"}).encode())

    def do_POST(self):
        """ Handle POST request to add a new task """
        if self.path == "/tasks":
            content_length = int(self.headers['Content-Length'])
            post_data = json.loads(self.rfile.read(content_length).decode())
            
            title = post_data.get("title")
            if not title:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Title is required"}).encode())
                return

            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tasks (title) VALUES (%s)", (title,))
            conn.commit()
            conn.close()

            self._set_headers(201)
            self.wfile.write(json.dumps({"message": "Task added"}).encode())

    def do_PUT(self):
        """ Handle PUT request to update a task """
        parsed_url = urlparse(self.path)
        if parsed_url.path.startswith("/tasks/"):
            task_id = parsed_url.path.split("/")[-1]
            content_length = int(self.headers['Content-Length'])
            put_data = json.loads(self.rfile.read(content_length).decode())
            status = put_data.get("status")

            if status not in ["pending", "completed"]:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Invalid status"}).encode())
                return

            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("UPDATE tasks SET status = %s WHERE id = %s", (status, task_id))
            conn.commit()
            conn.close()

            self._set_headers(200)
            self.wfile.write(json.dumps({"message": "Task updated"}).encode())

    def do_DELETE(self):
        """ Handle DELETE request to remove a task """
        parsed_url = urlparse(self.path)
        if parsed_url.path.startswith("/tasks/"):
            task_id = parsed_url.path.split("/")[-1]

            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
            conn.commit()
            conn.close()

            self._set_headers(200)
            self.wfile.write(json.dumps({"message": "Task deleted"}).encode())

# Run the server
def run(server_class=HTTPServer, handler_class=TodoHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()