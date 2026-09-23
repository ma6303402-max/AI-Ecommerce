from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.views import View
from .forms import CustomerRegistrationForm, CustomLoginForm

class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('products:catalog')
        form = CustomerRegistrationForm()
        return render(request, 'auth/register.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'customer'
            user.save()
            login(request, user)
            messages.success(request, f"Welcome to AI Store, {user.username}! Account created successfully.")
            return redirect('products:catalog')
        return render(request, 'auth/register.html', {'form': form})

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('products:catalog')
        form = CustomLoginForm()
        return render(request, 'auth/login.html', {'form': form})

    def post(self, request):
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('products:catalog')
        messages.error(request, "Invalid username or password.")
        return render(request, 'auth/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('products:catalog')
