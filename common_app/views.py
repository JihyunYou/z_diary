from django.contrib import auth
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect


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
