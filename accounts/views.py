from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    login,
    logout,
)
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from .forms import (
    UserLoginForm, UserRegistrationForm,
    AccountDetailsForm, UserAddressForm,
)
from .models import User

from .forms import UserLoginForm

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm, AccountDetailsForm, UserAddressForm

def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        user_form = UserRegistrationForm(request.POST or None)
        account_form = AccountDetailsForm(request.POST or None, request.FILES or None)
        address_form = UserAddressForm(request.POST or None)

        if user_form.is_valid() and account_form.is_valid() and address_form.is_valid():
            user = user_form.save()
            account_details = account_form.save(commit=False)
            address = address_form.save(commit=False)
            account_details.user = user
            account_details.account_no = user.username
            account_details.save()
            address.user = user

            # Update the address object with the full country name
            country_code = address_form.cleaned_data.get("country")
            country_name = dict(address_form.fields["country"].choices)[country_code]
            address.country = country_name

            address.save()

            # Save the user picture
            if account_form.cleaned_data.get("picture"):
                account_details.picture = account_form.cleaned_data.get("picture")
                account_details.save()

            new_user = authenticate(
                username=user.username, password=user_form.cleaned_data.get("password1")
            )
            login(request, new_user)
            messages.success(
                request,
                f"Thank you for creating a bank account {new_user.full_name}. "
                f"Your username is {new_user.username}. Please use this number to login."
            )
            return redirect("home")

        context = {
            "title": "Create a Bank Account",
            "user_form": user_form,
            "account_form": account_form,
            "address_form": address_form,
        }

        return render(request, "accounts/register_form.html", context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        form = UserLoginForm(request.POST or None)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            # authenticate with username/email and password
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, 'Welcome, {}!'.format(user.get_full_name()))
                return redirect("home")

        context = {"form": form,
                   "title": "Log in",
                   }

        return render(request, "accounts/form.html", context)

def logout_view(request):
    if not request.user.is_authenticated:
        return redirect("accounts:login")
    else:
        logout(request)
        return redirect("home")

    
def select_user(request):
    users = User.objects.all()
    return render(request, 'accounts/select_user.html', {'users': users})    
