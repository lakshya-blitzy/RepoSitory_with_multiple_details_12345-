from flask import Flask

app = Flask(__name__, static_folder=None)

METHODS = ["GET", "HEAD", "POST", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE", "PATCH"]
BODY = "Hello, World!\n"


@app.route("/", defaults={"path": ""}, methods=METHODS)
@app.route("/<path:path>", methods=METHODS)
def hello(path):
    return BODY


print("Server running at http://127.0.0.1:3000/")
app.run(port=3000)
