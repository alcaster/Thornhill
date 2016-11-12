import smtplib
from smtplib import SMTPAuthenticationError
from email.mime.multipart import MIMEMultipart
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

    def send_message(self, to_mail, subject, message, attachment=None):
        msg = self.compose_message(self.from_mail, to_mail, subject, message, attachment)
        with open_server(self.host, self.username, self.password) as server:
            if server:
                server.sendmail(self.from_mail, to_mail, msg)

    @staticmethod
    def compose_message(from_mail, to_mail, subject, message, attachment):
        msg = MIMEMultipart()
        msg['From'] = from_mail
        msg['To'] = to_mail
        msg['Subject'] = subject
        body = message
        msg.attach(MIMEText(body, 'plain'))
        if attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            filename = attachment.name
            part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
            msg.attach(part)
        return msg.as_string()

# if __name__ == "__main__":
#     s = Sender('chaleckim@student.mini.pw.edu.pl')
#     s.send_message(to_mail="chaleckim@student.mini.pw.edu.pl", subject="TEMAT", message="WIADOMOSC")
