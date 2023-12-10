from flask import Flask, render_template, request, redirect, url_for
import socket
import json
from datetime import datetime
from threading import Thread

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/imessage")
def imessage():
    return render_template("imessage.html")

@app.route("/message", methods=["POST"])
def message():
    username = request.form['username']
    message_content = request.form["message"]

    send_to_socket({"username": username, "message": message_content})

    return redirect(url_for("imessage"))

@app.errorhandler(404)
def not_found_error(error):
    return render_template("error.html"), 404



def socket_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(("localhost", 5000))

    while True:
        data, addr = server_socket.recvfrom(1024)
        data_dict = json.loads(data.decode("utf-8"))
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

        with open("storage/data.json", "a") as json_file:
            json.dump({timestamp: data_dict}, json_file)
            json_file.write("\n")

def send_to_socket(data):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.sendto(json.dumps(data).encode("utf-8"),("localhost", 5000))

if __name__ == "__main__":
    socket_thread = Thread(target=socket_server)
    socket_thread.start()

    app.run(port=3000)