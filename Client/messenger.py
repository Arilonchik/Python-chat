from datetime import datetime
import requests
from PyQt5 import QtWidgets
from Client import mainui


class MessengerApp(QtWidgets.QMainWindow, mainui.Ui_Dialog):
    """
    MessengerApp -UI window class.
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.last_time = 0
        self.pushButton.pressed.connect(self.button_clicked)
        self.pushButton_2.pressed.connect(self.update_messages_iteration)

    def send_message(self, username, password, text):
        """ Sending messages."""
        response = requests.post(
            "http://127.0.0.1:5000/auth",
            json={"username": username, "password": password}
        )
        if not response.json()['ok']:
            self.add_to_chat('Сообщение не отправлено')
            return

        response = requests.post(
            "http://127.0.0.1:5000/send",
            json={"username": username, "password": password, "text": text}
        )
        if not response.json()['ok']:
            self.add_to_chat('Сообщение не отправлено')

    def update_messages_iteration(self):
        """ Update chat."""
        response = requests.get("http://127.0.0.1:5000/messages",
                                params={'after': self.last_time})
        messages = response.json()["messages"]

        for message in messages:
            beauty_time = datetime.fromtimestamp(message["time"])
            beauty_time = beauty_time.strftime('%d/%m/%Y %H:%M:%S')
            self.add_to_chat(message["username"] + ' ' + beauty_time)
            self.add_to_chat(message["text"])
            self.add_to_chat('')
            self.last_time = message["time"]

    def button_clicked(self):
        """ Button "send' behavior. """
        try:
            self.send_message(
                self.textEdit.toPlainText(),
                self.textEdit_2.toPlainText(),
                self.textEdit_3.toPlainText()
            )
        except:
            self.add_to_chat('Произошла ошибка')

        self.textEdit_3.setText('')
        self.textEdit_3.repaint()

    def add_to_chat(self, text):
        """ Update main window (chat)."""
        self.textBrowser.append(text)
        self.textBrowser.repaint()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MessengerApp()
    window.show()
    app.exec_()
