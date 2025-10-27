import http.server
import socketserver
import requests

PORT = 8080
TARGET = "https://el-guero-0xdeadcode-mirror.onrender.com"

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        url = TARGET + self.path
        try:
            response = requests.get(url, verify=False)
            self.send_response(response.status_code)
            for key, value in response.headers.items():
                if key.lower() not in ['content-encoding', 'transfer-encoding', 'content-length']:
                    self.send_header(key, value)
            self.end_headers()
            self.wfile.write(response.content)
        except Exception as e:
            self.send_error(500, f"Proxy error: {e}")

with socketserver.TCPServer(("", PORT), ProxyHandler) as httpd:
    print(f"✅ Proxy running on port {PORT}, forwarding to {TARGET}")
    httpd.serve_forever()
