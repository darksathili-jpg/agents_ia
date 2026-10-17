"""Serveur de démonstration local ; aucune publication sur Internet."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import threading
import webbrowser

parser = argparse.ArgumentParser(description="Ouvrir Agent Academy localement")
parser.add_argument("--port", type=int, default=8765)
parser.add_argument("--sans-navigateur", action="store_true")
args = parser.parse_args()
root = Path(__file__).resolve().parent.parent
try:
    server = ThreadingHTTPServer(("127.0.0.1", args.port), partial(SimpleHTTPRequestHandler, directory=str(root)))
except OSError as error:
    parser.exit(1, f"Impossible de démarrer : {error}\nFermez le serveur précédent ou choisissez --port 8766.\n")
url = f"http://127.0.0.1:{server.server_port}/module01.html"
print(url, flush=True)
print("Laissez cette fenêtre ouverte. Ctrl+C arrête le serveur local.", flush=True)
if not args.sans_navigateur:
    threading.Timer(0.5, lambda: webbrowser.open(url)).start()
try:
    server.serve_forever()
except KeyboardInterrupt:
    pass
finally:
    server.server_close()
