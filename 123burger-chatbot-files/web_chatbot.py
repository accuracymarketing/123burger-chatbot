"""Tiny web server that exposes the restaurant chatbot to a website."""

from __future__ import annotations

import json
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from restaurant_chatbot import RESTAURANT_NAME, answer_question


ROOT = Path(__file__).parent
STATIC_DIR = ROOT / "static"


class ChatbotRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)

    def do_GET(self) -> None:
        if self.path == "/":
            self.path = "/demo.html"
        super().do_GET()

    def do_POST(self) -> None:
        if urlparse(self.path).path != "/chat":
            self.send_error(404, "Not found")
            return

        length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(length)

        try:
            payload = json.loads(raw_body.decode("utf-8"))
            message = str(payload.get("message", ""))
        except json.JSONDecodeError:
            self.send_json({"error": "Please send valid JSON."}, status=400)
            return

        self.send_json(
            {
                "restaurant": RESTAURANT_NAME,
                "answer": answer_question(message),
            }
        )

    def end_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        super().end_headers()

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.end_headers()

    def send_json(self, data: dict, status: int = 200) -> None:
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def run_server() -> None:
    host = "0.0.0.0"
    port = int(os.environ.get("PORT", "8000"))
    server = ThreadingHTTPServer((host, port), ChatbotRequestHandler)
    print(f"Restaurant chatbot website demo running on port {port}")
    print("Press Ctrl+C to stop the server.")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
