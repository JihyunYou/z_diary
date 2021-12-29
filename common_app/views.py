from django.contrib import auth
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect

from common_app.models import User


def index(request):
    return render(
        request,
        'common_app/index.html',
    )


def dev_alert(request):
    return render(
        request,
        'common_app/dev_alert.html',
    )


def login(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect(index)
        else:
            return render(
                request,
                'common_app/login.html',
                {
                    'error': '로그인 정보가 잘못되었습니다'
                }
            )

    else:
        return render(request, 'common_app/login.html')


def logout(request):
    auth.logout(request)
    return redirect(index)


def signup(request):
    context = {}

    if request.POST:
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        name = request.POST['username']

        try:
            User.objects.get(email=email)
            error = "이미 가입된 메일입니다!"
            context['error'] = error

            return render(
                request,
                'common_app/sign_up.html',
                context
            )
        except:
            pass

        if password1 != password2:
            error = "비밀번호가 서로 다릅니다!"
            context['error'] = error

            return render(
                request,
                'common_app/sign_up.html',
                context
            )

        # 생성
        user = User.objects.create_user(
            email=email,
            name=name,
            password=password1
        )
        auth.login(request, user)
        return redirect('/')

    return render(
        request,
        'common_app/sign_up.html',
        context
    )