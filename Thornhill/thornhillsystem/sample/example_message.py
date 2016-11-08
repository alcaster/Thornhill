import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
from contextlib import contextmanager
import ntpath


@contextmanager
def open_server(host, username, password):
    server = smtplib.SMTP(host)

    server.ehlo()

    server.starttls()
    server.login(username, password)
    yield server
    server.quit()


def path_leaf(path):
    """Used to change filepath to filename"""
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def send_message(to_mail, subject, message):
    from_mail = 'chaleckim@student.mini.pw.edu.pl'
    username = 'chaleckim'
    password = "BcpVpV2b"
    host = "poczta.mini.pw.edu.pl:587"
    msg = compose_message(from_mail, to_mail, subject, message,
                          "/home/alcaster/Projects/raspberry/Thornhill/thornhillsystem/sample/no_utrudnienia")

    with open_server(host, username, password) as server:
        server.sendmail(from_mail, to_mail, msg)


def compose_message(from_mail, to_mail, subject, message, attachment_path=None):
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
        filename = path_leaf(attachment_path)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(part)
    return msg.as_string()


if __name__ == "__main__":
    send_message(to_mail="chaleckim@student.mini.pw.edu.pl", subject="TEMAT", message="WIADOMOSC")
