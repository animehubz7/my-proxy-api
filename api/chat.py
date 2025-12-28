from http.server import BaseHTTPRequestHandler
import json
import requests
import uuid

TARGET_API = "https://api.acix.site/chat"
API_KEY = "ACIF58NKNN"

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length"))
            body = self.rfile.read(length)
            data = json.loads(body)

            msg = data.get("message", "")
            uid = str(uuid.uuid4())

            r = requests.get(
                TARGET_API,
                params={
                    "apikey": API_KEY,
                    "uid": uid,
                    "msg": msg
                },
                headers={
                    "User-Agent": "Mozilla/5.0"
                },
                timeout=15
            )

            try:
                reply = r.json().get("reply", "")
            except:
                reply = r.text

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(json.dumps({
                "reply": reply
            }).encode())

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": str(e)
            }).encode())
          
