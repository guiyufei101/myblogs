import smtplib
import string

HOST = "smtp.gmail.com"
SUBJECT = "Test email from Python"
TO = "1963119101@qq.com"
FROM = "guiyufei1@gmail.com"
text = "Python rules them all!"
BODY = "\r\n".join((
    "From: %s" % FROM,
    "To: %s" % TO,
    "Subject: %s" % SUBJECT,
    "",
    text
))
server = smtplib.SMTP()
server.connect(HOST, "25")
server.starttls()
server.login("guiyufei1@gmail.com", "gui319861")
server.sendmail(FROM, [TO], BODY)
server.quit()