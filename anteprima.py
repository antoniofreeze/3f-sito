#!/usr/bin/env python3
"""Anteprima locale che imita GitHub Pages: /storia serve storia.html, gli indirizzi inesistenti servono 404.html."""
import http.server, os, sys
porta = int(sys.argv[1]) if len(sys.argv) > 1 else 4412
os.chdir(sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(os.path.abspath(__file__)))
class H(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        p = self.path.split('?')[0].split('#')[0]
        loc = '.' + p
        if p != '/' and not os.path.exists(loc) and os.path.exists(loc + '.html'):
            self.path = p + '.html'
        elif not os.path.exists(loc):
            self.send_response(404); self.send_header('Content-Type', 'text/html; charset=utf-8'); self.end_headers()
            self.wfile.write(open('404.html', 'rb').read()); return
        super().do_GET()
    def log_message(self, *a): pass
http.server.ThreadingHTTPServer(('127.0.0.1', porta), H).serve_forever()
