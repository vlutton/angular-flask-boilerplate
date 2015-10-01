from flask import render_template
from flask_mail import Mail, Message

def send_email(subject, sender, recipients, text_body, html_body):
    mail = Mail()
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

def send_confirmation_email(confirmation_url, user):
	send_email("Please confirm your account", "vincelutton@gmail.com", [user.email],
				render_template("confirmation_email.txt",
								confirmation_url=confirmation_url, user=user),
				render_template("confirmation_email.html",
								confirmation_url=confirmation_url, user=user))
