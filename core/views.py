from django.db.models import Sum
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from transactions.models import *
from accounts.models import User

def home(request):
    users = User.objects.all()

    if not request.user.is_authenticated:
        return render(request, "core/index.html", {})
    else:
        user = request.user
        deposit = Diposit.objects.filter(user=user)
        deposit_sum = deposit.aggregate(Sum('amount'))['amount__sum']
        withdrawal = Withdrawal.objects.filter(user=user)
        withdrawal_sum = withdrawal.aggregate(Sum('amount'))['amount__sum']
        interest = Interest.objects.filter(user=user)
        interest_sum = interest.aggregate(Sum('amount'))['amount__sum']

        context = {
            "user": user,
            "deposit": deposit,
            "deposit_sum": deposit_sum,
            "withdrawal": withdrawal,
            "withdrawal_sum": withdrawal_sum,
            "interest": interest,
            "interest_sum": interest_sum,
            "users": users,  # Added users to the context
            "title": "ROYAL BANK"
        }

        return render(request, "core/transactions.html", context)

    
def about(request):
    return render(request, "core/about.html", {})

def contact_us(request):
    return render(request, "core/contact_us.html", {})



@login_required
def confirm(request):
    payment = Withdrawal.objects.filter(user=request.user).order_by('-id').first()
    return render(request, 'core/confirm.html', {'payment': payment})


@login_required
def inter_confirm(request):
    payment = Withdrawal_internationa.objects.filter(user=request.user).order_by('-id').first()
    return render(request, 'core/inter_confirm.html', {'payment': payment})


def confirm_password(request):
    return render(request, "core/confirm_password.html", {})
