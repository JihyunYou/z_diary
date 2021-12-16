from bootstrap_datepicker_plus import widgets
from bootstrap_datepicker_plus.widgets import DatePickerInput
from django.forms import ModelForm
from django.shortcuts import render, redirect

from account_book_app.models import Category, Account


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
            'date': DatePickerInput(format='%Y-%m-%d'),
        }


def show_contents(request):
    # 로그인 하지 않은 사용자가 URL을 통해 회원을 삭제하는 것을 막음
    # if not request.user.is_authenticated:
    #     print("권한 없는 사용자의 일정 등록 차단")
    #     return redirect('/')

    context = {}
    category_objs = Category.objects.all()
    account_objs = Account.objects.filter(user_id=request.user.id)
    account_form = AccountForm

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
    context['income'] = income
    context['expense'] = expense
    context['total'] = total

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
