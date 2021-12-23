import json
from datetime import datetime

from bootstrap_datepicker_plus import widgets
from bootstrap_datepicker_plus.widgets import DatePickerInput, MonthPickerInput
from django.forms import ModelForm
from django import forms
from django.http import HttpResponse
from django.shortcuts import render, redirect

from account_book_app.models import Category, Account


class DateForm(forms.Form):
    input_date = forms.DateField(
        input_formats=['%Y-%m-%d'],
        label='원하는 월을 고르세요',
        widget=MonthPickerInput(
            attrs={
                'id': 'input_date',
            },
            options={
                'format': 'YYYY-MM',
                'locale': 'ko',
            }
        )
    )


class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = [
            'date',
            'category_id',
            'amount',
            'description',
        ]
        labels = {
            'date': '일자',
            'category_id': '범주',
            'amount': '금액',
            'description': '설명',
        }
        widgets = {
            'date': DatePickerInput(
                options={
                    'format': 'YYYY-MM-DD',
                    'locale': 'ko',
                }
            ),
        }


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = [
            'name',
        ]
        labels = {
            'name': '항목명'
        }


def show_contents(request):
    context = {}
    account_form = AccountForm
    category_form = CategoryForm
    date_form = DateForm

    category_objs = Category.objects.all()

    account_year = ''
    account_month = ''
    if request.POST:
        input_date = request.POST['input_date'].split('-')
        input_year = input_date[0]
        input_month = input_date[1]

        account_objs = Account.objects.filter(
            user_id=request.user.id,
            date__year=input_year,
            date__month=input_month,
        )
        account_year = input_year
        account_month = input_month
    else:
        account_objs = Account.objects.filter(
            user_id=request.user.id,
            date__year=datetime.today().year,
            date__month=datetime.today().month,
        )
        account_year = datetime.today().year
        account_month = datetime.today().month

    income = 0
    expense = 0
    for account in account_objs:
        if account.amount >= 0:
            income += account.amount
        else:
            expense += account.amount

    total = income + expense

    context['category_objs'] = category_objs
    context['account_objs'] = account_objs
    context['account_form'] = account_form
    context['category_form'] = category_form

    context['date_form'] = date_form

    context['income'] = income
    context['expense'] = expense
    context['total'] = total

    context['account_year'] = account_year
    context['account_month'] = account_month

    return render(
        request,
        'account_book_app/account_book_contents.html',
        context,
    )


def add_account(request):
    # 로그인 하지 않은 사용자가 URL을 통해 회원을 삭제하는 것을 막음
    if not request.user.is_authenticated:
        print("권한 없는 사용자의 가계부 내용 등록 차단")
        return redirect(show_contents)

    if request.POST:
        account_form = AccountForm(request.POST or None)
        if account_form.is_valid():
            account = account_form.save(commit=False)

            account.user_id = request.user
            account.created_by = request.user

            account.save()

            return redirect(show_contents)

    return redirect(show_contents)


def del_account(request):
    # 로그인 하지 않은 사용자가 URL을 통해 회원을 삭제하는 것을 막음
    if not request.user.is_authenticated:
        print("권한 없는 사용자의 가계부 내용 등록 차단")
        return redirect(show_contents)

    if request.POST:
        account_obj = Account.objects.get(pk=request.POST['account_id'])
        if account_obj is not None:
            account_obj.delete()

    return redirect(show_contents)


def add_category(request):
    # 로그인 하지 않은 사용자가 URL을 통해 회원을 삭제하는 것을 막음
    if not request.user.is_authenticated:
        print("권한 없는 사용자의 가계부 내용 등록 차단")
        return redirect(show_contents)

    if request.POST:
        category_form = CategoryForm(request.POST or None)
        if category_form.is_valid():
            category = category_form.save(commit=False)

            category.created_by = request.user

            category.save()

            return redirect(show_contents)

    return redirect(show_contents)


def del_category(request):
    # 로그인 하지 않은 사용자가 URL을 통해 회원을 삭제하는 것을 막음
    if not request.user.is_authenticated:
        print("권한 없는 사용자의 가계부 내용 등록 차단")
        return redirect(show_contents)

    if request.POST:
        category_obj = Category.objects.get(pk=request.POST['category_id'])
        if category_obj is not None:
            category_obj.delete()

    return redirect(show_contents)