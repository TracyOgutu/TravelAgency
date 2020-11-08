import os
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.template.loader import render_to_string
from django.core.mail import send_mail

def subscribe_email(name,receiver):
    message=Mail(
        from_email="beastmater064@gmail.com",
        to_emails=receiver,
        subject="Welcome to Travel Agency.",
        html_content=render_to_string('email.html',{"name":name})
    )
    sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)

    
def send_email(subject,usermessage,name,sender):
    message_x = Mail(
        from_email=sender,
        to_emails='beastmater064@gmail.com',
        subject=subject,
        html_content=render_to_string('send_mail.html',{"name":name,"message":usermessage})
    )
    sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
    response = sg.send(message_x)
    print(response.status_code)
    print(response.body)
    print(response.headers)


    
 
  