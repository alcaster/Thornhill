import smtplib
from smtplib import SMTPAuthenticationError
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
from contextlib import contextmanager
import ntpath
import json


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


class Sender:
    def __init__(self, account):
        with open('accounts.json') as data_file:
            data = json.load(data_file)
        try:
            self.host = data[str(account)]["host"]
            self.username = data[str(account)]["username"]
            self.password = data[str(account)]["password"]
            self.from_mail = data[str(account)]["from_mail"]
        except KeyError:
            print('No such account')

    def path_leaf(self, path):
        """Used to change filepath to filename"""
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

    def send_message(self, to_mail, subject, message):
        msg = self.compose_message(self.from_mail, to_mail, subject, message,
                                   "/home/alcaster/Projects/raspberry/Thornhill/thornhillsystem/sample/no_utrudnienia")

        with open_server(self.host, self.username, self.password) as server:
            if server
                server.sendmail(self.from_mail, to_mail, msg)

    def compose_message(self, from_mail, to_mail, subject, message, attachment_path=None):
        msg = MIMEMultipart()
        msg['From'] = from_mail
        msg['To'] = to_mail
        msg['Subject'] = subject
        body = message
        msg.attach(MIMEText(body, 'plain'))
        if attachment_path:
            attachment = open(attachment_path, "rb")
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            filename = self.path_leaf(attachment_path)
            part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
            msg.attach(part)
        return msg.as_string()
#
#
# if __name__ == "__main__":
#     s = Sender('chaleckim@student.mini.pw.edu.pl')
#     s.send_message(to_mail="chaleckim@student.mini.pw.edu.pl", subject="TEMAT", message="WIADOMOSC")
