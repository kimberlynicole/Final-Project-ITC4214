from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .models import Profile
from .forms import ProfileForm

# Create your views here.


# Register View
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Create profile manually
        Profile.objects.create(user=user, email=email)

        # Log the user in
        login(request, user)

        return redirect('dashboard')

    return render(request, 'accounts/register.html')


# Login View
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'accounts/login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'accounts/login.html')


#  Logout View
def user_logout(request):
    logout(request)
    return redirect('login')


# 🔹 Dashboard View
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'accounts/dashboard.html')


#  Profile View (View + Update)
def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')

    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'accounts/profile.html', {'form': form})