from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string

# Create your views here.

def send(recieverEmail, verifyCode):
    try:
        content={'verifyCode': verifyCode}
        msg_html=render_to_string("sendEmail/email_format.html", content)
        msg = EmailMessage(subject="[멀티캠퍼스] 인증코드 발송 메일",
                           body=msg_html,
                           from_email="kitbung0214@gmail.com",
                           bcc=[recieverEmail])
        msg.content_subtype ='html'
        msg.send()
        return True
    except:
        return False

