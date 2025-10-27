import http.server
import socketserver
import requests
from urllib.parse import urljoin

PORT = 8080
TARGET = "https://el-guero-0xdeadcode-mirror.onrender.com"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
}

class ProxyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        url = urljoin(TARGET, self.path)
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)

            self.send_response(response.status_code)
            # Pass through most headers unchanged
            for key, value in response.headers.items():
                if key.lower() not in ['transfer-encoding', 'content-encoding', 'connection']:
                    self.send_header(key, value)
            self.end_headers()

            # Write raw bytes exactly as received (no decoding)
            self.wfile.write(response.content)

        except Exception as e:
            self.send_error(500, f"Proxy error: {e}")

with socketserver.TCPServer(("127.0.0.1", PORT), ProxyHandler) as httpd:
    print(f"✅ Serving raw proxy on http://127.0.0.1:{PORT}")
    print(f"→ Forwarding to {TARGET}")
    httpd.serve_forever()
