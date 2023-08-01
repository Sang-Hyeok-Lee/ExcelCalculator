from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from random import *
from sendEmail.views import *


# Create your views here.
def index(request):
    return render(request, 'main/index.html')

def signup(request):
    return render(request, 'main/signup.html')

def join(request):
    print(request)
    name=request.POST['signupName']
    email=request.POST['signupEmail']
    pw=request.POST['signupPW']
    user=User(user_name=name, user_email=email, user_password = pw)
    user.save()
    print("사용자 정보 저장 완료됨!!")
    #인증코드 하나 생성
    code = randint(1000,9999)
    response = redirect("main_verifyCode")
    response.set_cookie('code', code)
    response.set_cookie('user_id', user.id)  
    send_result = send(email,code)
    if send_result:
        print("Main > views.py > 이메일 발송 중 완료된 거 같음...")
        return response
    else:
        return HttpResponse("이메일 발송 실패!")


def signin(request):
    return render(request, 'main/signin.html')

def verifyCode(request):
    return render(request, 'main/verifyCode.html')

def verify(request):
    # 사용자가 입력한 code값을 받아야 함
    user_code = request.POST['verifyCode']
    # 사용자 코드와 쿠키 코드를 매칭해야함
    cookie_code=request.COOKIES.get('code')
    print("코드확인:", user_code, cookie_code)

    if user_code == cookie_code:
        user= User.objects.get(id=request.COOKIES.get('user_id'))
        user.user_validate = 1
        user.save()
        
        print("DB에 user_validate 업데이트-----------------")

        response = redirect('main_index')

        # 저장된 쿠키를 삭제
        response.delete_cookie('code')
        response.delete_cookie('user_id')
        # response.set_cookie('user',user)

        # 사용자 정보를 세션에 저장
        request.session['user_name']=user.user_name   ## 로그인 화면 구현
        request.session['user_email']=user.user_email ## 로그인 화면 구현
        return response

    else:
        return redirect('verifyCode') # verifycode 화면으로 돌리기

def result(request):
    return render(request, 'main/result.html')