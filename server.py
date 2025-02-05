import sys
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/snooker.html':
            try:
                # Open the snooker.html file
                with open('snooker.html', 'rb') as file:
                    content = file.read()
                # Send HTTP response for HTML content
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.send_header('Content-length', len(content))
                self.end_headers()
                self.wfile.write(content)
            except FileNotFoundError:
                # If file not found, send 404 response
                self.send_error(404, 'File not found')
        else:
            # For other paths, send 404 response
            self.send_error(404, 'File not found')

# Main block for running the server
if __name__ == '__main__':
    try:
        # Create an instance of the HTTPServer
        httpd = HTTPServer(('localhost', int(sys.argv[1])), MyHandler)
        print('Server listening on port:', int(sys.argv[1]))
        # Start the server
        httpd.serve_forever()
    except KeyboardInterrupt:
        # Handle keyboard interrupt (Ctrl+C) to stop the server
        print('Server stopped')
        httpd.server_close()