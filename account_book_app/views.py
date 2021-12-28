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
        label='조회할 월을 고르세요',
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
            'description',
        ]
        labels = {
            'name': '항목명',
            'description': '설명'
        }


def show_contents(request):
    context = {}
    account_form = AccountForm
    category_form = CategoryForm
    date_form = DateForm

    category_objs = Category.objects.filter(
        created_by=request.user
    )

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

    category_sum = Account.get_sum_by_category(
        None,
        request.user.id,
        account_year,
        account_month
    )

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
    context['category_sum'] = category_sum
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


def account_detail(request, account_id):
    # 로그인 하지 않은 사용자가 URL을 통해 회원을 삭제하는 것을 막음
    if not request.user.is_authenticated:
        print("권한 없는 사용자의 가계부 내용 등록 차단")
        return redirect(show_contents)

    context = {}
    account_obj = Account.objects.get(pk=account_id)

    account_form = AccountForm(request.POST or None, instance=account_obj)
    if account_form.is_valid():
        account_form.save()
        return redirect(account_detail, account_id=account_id)

    context['account_obj'] = account_obj
    context['account_form'] = account_form

    return render(
        request,
        'account_book_app/account_detail.html',
        context,
    )


def category_detail(request, category_id):
    # 로그인 하지 않은 사용자가 URL을 통해 회원을 삭제하는 것을 막음
    if not request.user.is_authenticated:
        print("권한 없는 사용자의 가계부 내용 등록 차단")
        return redirect(show_contents)

    context = {}
    category_objs = Category.objects.filter(created_by=request.user)
    category_obj = Category.objects.get(pk=category_id)

    category_form = CategoryForm(request.POST or None, instance=category_obj)
    if category_form.is_valid():
        category_form.save()
        return redirect(category_detail, category_id=category_id)

    context['category_objs'] = category_objs
    context['category_obj'] = category_obj
    context['category_form'] = category_form

    return render(
        request,
        'account_book_app/category_detail.html',
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


def update_account(request):
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

            # Order 값 설정
            count = Category.objects.filter(created_by=request.user).count()
            count += 1
            category.order = count

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


def set_category_order(request, category_id):
    # 로그인 하지 않은 사용자가 URL을 통해 회원을 삭제하는 것을 막음
    if not request.user.is_authenticated:
        print("권한 없는 사용자의 가계부 내용 등록 차단")
        return redirect(show_contents)

    if request.POST:
        current_order = request.POST['category_order']
        action_type = request.POST['action_type']
        if action_type == "up":
            new_order = int(current_order) - 1
        else:
            new_order = int(current_order) + 1

        try:
            old_category_obj = Category.objects.get(
                created_by=request.user,
                order=current_order
            )
            new_category_obj = Category.objects.get(
                created_by=request.user,
                order=new_order
            )

            old_category_obj.order = 0
            old_category_obj.save()

            new_category_obj.order = int(current_order)
            new_category_obj.save()

            old_category_obj.order = new_order
            old_category_obj.save()

        except:
            print("잘못된 입력")

        return redirect(category_detail, category_id)

    return redirect(show_contents)
