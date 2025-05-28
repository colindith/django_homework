from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .forms import LoginForm

def user_login_view(request):
    if request.user.is_authenticated:
        return redirect('apply')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                # login the user
                login(request, user)
                return redirect('apply')
            else:
                messages.error(request, 'invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def user_logout_view(request):
    logout(request)
    messages.success(request, "You are logged out successfully")
    return redirect('user_login')