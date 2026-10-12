"""Isolated metrics + webhook lab; must NOT receive production secrets."""
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import json

STATE = Path('/app/status.json')


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != '/metrics':
            self.send_error(404)
            return
        try:
            state = json.loads(STATE.read_text(encoding='utf-8'))
            metrics = (
                '# TYPE shop_lab_api_healthy gauge\n'
                f"shop_lab_api_healthy {int(state.get('api_healthy', 1))}\n"
                '# TYPE shop_lab_payment_error_ratio gauge\n'
                f"shop_lab_payment_error_ratio {float(state.get('payment_error_ratio', 0.0))}\n"
            ).encode()
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; version=0.0.4')
            self.send_header('Content-Length', str(len(metrics)))
            self.end_headers()
            self.wfile.write(metrics)
        except (OSError, ValueError, TypeError):
            self.send_error(500, 'invalid lab state')

    def do_POST(self):
        if self.path != '/alert':
            self.send_error(404)
            return
        if int(self.headers.get('Content-Length', '0')) > 8192:
            self.send_error(413)
            return
        self.rfile.read(int(self.headers.get('Content-Length', '0')))
        print('Synthetic test webhook received; payload not logged', flush=True)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')


if __name__ == '__main__':
    HTTPServer(('0.0.0.0', 9108), Handler).serve_forever()
