from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def send(recieverEmail, verifyCode):
    return HttpResponse("sendEmail, send function!")