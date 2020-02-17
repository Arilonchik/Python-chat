import time
from datetime import datetime
import Server.database as dt
from flask import Flask, request

app = Flask(__name__)

# Connection to postgres, loads users chat
users, messages, conn = dt.connect_base()
cursor = conn.cursor()


@app.route("/")
def hello_view():
    return "<h1>Welcome to Python messenger!</h1>"


@app.route("/status")
def status_view():
    """
    Checking server status, number of users and messages.
    """
    srv_status = {'status': True,
                  'time': datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
    return "Status: " + str(srv_status['status']) + '<br>' + 'Time: ' + str(srv_status['time']) + '<br>' + 'Messages ' \
           'in chat now: ' + str(len(messages)) + '<br>' + 'Users registered in chat: ' + str(len(users))


@app.route("/messages")
def messages_view():
    """
    Loads messages after flag "after".
    input: after - time flag
    output: {
        "messages": [
            {"username": str, "text": str, "time": float},
            ...
        ]
    }
    """
    after = float(request.args['after'])
    new_messages = [message for message in messages if message['time'] > after]
    return {'messages': new_messages}


@app.route("/send", methods=['POST'])
def send_view():
    """
    Sending messages.
    input: {
        "username": str,
        "password": str,
        "text": str
    }
    output: {"ok": bool}
    """
    data = request.json
    username = data["username"]
    password = data["password"]

    if username not in users or users[username] != password:
        return {"ok": False}

    text = data["text"]
    messages.append({"username": username, "text": text, "time": time.time()})

    sql = "INSERT INTO messages VALUES ( \'{}\',\'{}\',\'{}\')".format(username, text, time.time())
    cursor.execute(sql)
    conn.commit()

    return {'ok': True}


@app.route("/auth", methods=['POST'])
def auth_view():
    """
    User authorization.
    input: {
        "username": str,
        "password": str
    }
    output: {"ok": bool}
    """
    data = request.json
    username = data["username"]
    password = data["password"]

    if username not in users:
        users[username] = password
        sql = "INSERT INTO users VALUES ( \'{}\',\'{}\')".format(username, password)
        cursor.execute(sql)
        conn.commit()
        return {"ok": True}
    elif users[username] == password:
        return {"ok": True}
    else:
        return {"ok": False}


if __name__ == '__main__':
    app.run()
