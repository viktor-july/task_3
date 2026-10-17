from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from math import gcd
import re
import os

EMAIL_PATH = "/viktor_july_protonmail_com"

def valid(s):
    return s is not None and re.fullmatch(r"0|[1-9]\d*", s) is not None

def lcm(a, b):
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // gcd(a, b)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if not parsed.path.rstrip("/").endswith(EMAIL_PATH.lstrip("/")):
            self.send_response(404)
            self.end_headers()
            return

        q = parse_qs(parsed.query)
        xs = q.get("x", [None])[0]
        ys = q.get("y", [None])[0]

        if valid(xs) and valid(ys):
            body = str(lcm(int(xs), int(ys)))
        else:
            body = "NaN"

        data = body.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *args):
        pass

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    HTTPServer(("", port), Handler).serve_forever()