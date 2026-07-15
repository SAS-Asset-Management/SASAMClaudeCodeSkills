#!/usr/bin/env python3
"""
serveDeck.py — serve a deck-stage v2 presentation locally for live delivery.

Why this exists: the presenter camera cameo uses getUserMedia, which the browser
only exposes in a SECURE CONTEXT. Chrome treats http://localhost as secure, so
plain HTTP is enough for Chrome. Safari (and camera access on any non-localhost
host) treats http://localhost as INSECURE — it needs https://. This script
serves HTTP by default and, with --https, serves TLS using an mkcert dev cert so
the cameo works in Safari too.

Usage
-----
  # Chrome, camera works on http://localhost:
  python3 serveDeck.py                 # serves the current dir on :8137

  # Safari (or any browser), camera needs https — one-time cert setup first:
  #   brew install mkcert            (if not installed)
  #   mkcert -install                (installs a local CA into the keychain;
  #                                   asks for the Mac password — one time)
  #   mkcert localhost 127.0.0.1     (writes localhost+1.pem / -key.pem here)
  python3 serveDeck.py --https        # serves https://localhost:8444
  #   Safari gotcha: if you visited the http site BEFORE `mkcert -install`,
  #   Safari cached the cert as untrusted. Fully QUIT and reopen Safari, and do
  #   NOT use a Private window (Private windows can block the camera).

Serve from the directory that CONTAINS presentation.html (and its engine/ and
assets/ folders). Then open the printed URL and toggle the Camera button.
"""
import argparse
import http.server
import os
import socketserver
import ssl
import sys

def main():
    ap = argparse.ArgumentParser(description="Serve a deck-stage deck locally.")
    ap.add_argument("--https", action="store_true", help="serve TLS with an mkcert cert (needed for Safari camera)")
    ap.add_argument("--port", type=int, default=None, help="override the port")
    ap.add_argument("--cert", default="localhost+1.pem", help="mkcert cert file (default: localhost+1.pem)")
    ap.add_argument("--key", default="localhost+1-key.pem", help="mkcert key file (default: localhost+1-key.pem)")
    ap.add_argument("--dir", default=".", help="directory to serve (default: current)")
    args = ap.parse_args()

    os.chdir(args.dir)
    port = args.port or (8444 if args.https else 8137)
    scheme = "https" if args.https else "http"

    handler = http.server.SimpleHTTPRequestHandler

    class Server(socketserver.TCPServer):
        allow_reuse_address = True

    httpd = Server(("0.0.0.0", port), handler)

    if args.https:
        if not (os.path.exists(args.cert) and os.path.exists(args.key)):
            sys.exit(
                "mkcert cert not found (%s / %s).\n"
                "Run:  mkcert -install   then   mkcert localhost 127.0.0.1\n"
                "in this directory, or pass --cert/--key." % (args.cert, args.key)
            )
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain(certfile=args.cert, keyfile=args.key)
        httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)

    url = "%s://localhost:%d/" % (scheme, port)
    print("Serving %s at %s  (Ctrl-C to stop)" % (os.getcwd(), url))
    if not args.https:
        print("Note: camera works here in Chrome only. For Safari, re-run with --https.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")

if __name__ == "__main__":
    main()
