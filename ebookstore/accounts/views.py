from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .forms import  RegisterForm, LoginForm
from django.contrib import messages

# Create your views here.
# Register View
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Create the user
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )
            login(request, user)  # auto-login after registration
            messages.success(request, f"Welcome {user.first_name}! Your account has been created.")
            return redirect('accounts:dashboard')
        else:
            # errors will be automatically passed to template
            messages.error(request, "Please fix the errors below")
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})

# Login View
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('accounts:dashboard')
            else:
                form.add_error('password', 'Username or password is incorrect')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {
        'form': form
    })


# Logout View
def user_logout(request):
    logout(request)
    return redirect('accounts:login')


# Dashboard View
def dashboard(request):
    if request.user.id is None:  # manual check instead of @login_required
        return redirect('accounts:login')

    # Use RegisterForm (or a ProfileForm without image) to update info
    if request.method == 'POST':
        form = RegisterForm(request.POST)  # or custom form for full_name/email
        if form.is_valid():
            request.user.username = form.cleaned_data['username']
            request.user.email = form.cleaned_data['email']
            # If you want, update password as well, see note below
            request.user.save()
            return redirect('accounts:dashboard')
    else:
        form = RegisterForm(initial={
            'username': request.user.username,
            'email': request.user.email,
        })

    return render(request, 'accounts/dashboard.html', {'form': form})
