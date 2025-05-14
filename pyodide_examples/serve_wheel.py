import http.server
import socketserver
import os

# Directory containing the PlantCV wheel file
DIRECTORY = "./wheels"

# Port to serve the files
PORT = 8000


# Custom handler to add CORS headers
class CORSHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()


# Change to the directory containing the wheel file
os.chdir(DIRECTORY)

# Set up the server
Handler = CORSHTTPRequestHandler
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    httpd.serve_forever()
