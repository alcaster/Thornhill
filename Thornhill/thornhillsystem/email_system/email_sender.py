import ntpath
import smtplib
from smtplib import SMTPAuthenticationError
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from contextlib import contextmanager
import json
import os
from Thornhill.celery import app


@contextmanager
def open_server(host, username, password):
    server = smtplib.SMTP(host)
    server.ehlo()
    server.starttls()
    try:
        server.login(username, password)
    except SMTPAuthenticationError:
        print("Wrong auth")
        server = None
    yield server
    server.quit()


def path_leaf(path):
    path = str(path)
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def get_all_accounts(filename):
    result = []
    path = os.path.dirname(os.path.realpath(__file__))
    with open(path + '/' + filename) as data_file:
        data = json.load(data_file)
        for account in data:
            result.append(account)
    return result


class Sender:
    def __init__(self, account):
        path = os.path.dirname(os.path.realpath(__file__))
        with open(path + '/accounts.json') as data_file:
            data = json.load(data_file)
        try:
            self.host = data[str(account)]["host"]
            self.username = data[str(account)]["username"]
            self.password = data[str(account)]["password"]
            self.from_mail = data[str(account)]["from_mail"]
        except KeyError:
            print('No such account')

    def send_message(self, to_mail, subject, message, attachment_path=None):
        msg = self.compose_message(self.from_mail, to_mail, subject, message, attachment_path)
        with open_server(self.host, self.username, self.password) as server:
            if server:
                server.sendmail(self.from_mail, to_mail, msg)

    @staticmethod
    def compose_message(from_mail, to_mail, subject, message, attachment_path):
        msg = MIMEMultipart()
        msg['From'] = from_mail
        msg['To'] = to_mail
        msg['Subject'] = subject
        body = message
        msg.attach(MIMEText(body, 'plain'))
        if attachment_path:
            name = path_leaf(attachment_path)
            with open(attachment_path, "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=name
                )
                part['Content-Disposition'] = 'attachment; filename="%s"' % name
                msg.attach(part)

        return msg.as_string()
