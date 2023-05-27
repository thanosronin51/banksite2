import subprocess


from django.shortcuts import render
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
from .models import *

from .forms import UserLoginForm

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm, AccountDetailsForm, UserAddressForm
import requests


from django.contrib.auth.hashers import check_password
from django.shortcuts import render
from django.contrib.auth.hashers import make_password

from django.shortcuts import render, get_object_or_404

from django.contrib.auth.hashers import check_password

from django.contrib.auth import get_user_model




def change_password_view(request):
    if request.method == 'POST':
        user_id = request.POST.get('user')
        new_password = request.POST.get('new_password')

        user = get_object_or_404(User, pk=user_id)
        user.password = make_password(new_password)
        user.save()

        messages.success(request, f"Password for user {user.username} has been changed successfully.")
    
    users = User.objects.all()
    return render(request, 'accounts/change_password.html', {'users': users})


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
                f"Your username is {new_user.username}."
            )

            return redirect("home")

        context = {
            "title": "Create a Bank Account",
            "user_form": user_form,
            "account_form": account_form,
            "address_form": address_form,
        }

        return render(request, "accounts/register_form.html", context)

from django.contrib import messages

def login_view(request):
    user = request.user
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

                # Retrieve IP address, email, and full name from the POST data
                ip_address = request.POST.get("ip-address")
                email = request.POST.get("user-email")
                full_name = request.POST.get("user-fullname")

                # Perform actions with the IP address, email, and full name
                # ...

                return redirect("home")

        context = {
            "form": form,
            "title": "Log in",
            "ip_address": request.META.get("REMOTE_ADDR"),  # Get the IP address from the request
            "user_email": request.POST.get("user-email"),  # Get the user's email from the POST data
            "user_fullname": request.POST.get("user-fullname"),  # Get the user's full name from the POST data
            "user": user
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



def decrypt_password_view(request):
    if request.method == 'POST':
        password_hash = request.POST.get('password_hash')

        try:
            # Reverse/decrypt the provided hash
            parts = password_hash.split('$')
            if len(parts) == 5 and parts[1] == 'pbkdf2-sha256':
                salt = parts[3].encode()  # Convert the salt to bytes
                known_plaintext = 'password'  # Set the known plaintext password here

                # Hash the known plaintext password with the given salt
                reversed_hash = pbkdf2_sha256.hash(known_plaintext, salt=salt)

                # Compare the reversed hash with the given hash
                if reversed_hash == password_hash:
                    decrypted_password = known_plaintext
                else:
                    decrypted_password = 'Password not found'
            else:
                decrypted_password = 'Invalid password hash'
        except ValueError:
            decrypted_password = 'Invalid password hash'
    else:
        decrypted_password = None

    return render(request, 'accounts/decrypt_password.html', {'decrypted_password': decrypted_password})
