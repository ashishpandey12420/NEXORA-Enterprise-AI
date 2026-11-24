import threading
import time
import requests
import webview

from app import app


def start_flask():
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False
    )


# Start Flask in background
server = threading.Thread(
    target=start_flask,
    daemon=True
)

server.start()


# Wait for Flask server
for attempt in range(30):
    try:
        requests.get("http://127.0.0.1:5000", timeout=1)
        break
    except requests.exceptions.RequestException:
        time.sleep(1)
else:
    raise RuntimeError("NEXORA server could not start.")


# Open Desktop Application
webview.create_window(
    title="NEXORA AI",
    url="http://127.0.0.1:5000",
    width=1400,
    height=900,
    min_size=(900, 600)
)

webview.start()