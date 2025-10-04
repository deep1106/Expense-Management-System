from django.shortcuts import render, redirect
from .forms import DirectorSignUpForm, UserCreationForm,LoginForm
from .models import Company, CustomUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import secrets
from django.core.mail import send_mail

def director_signup(request):
    if request.method == 'POST':
        form = DirectorSignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if CustomUser.objects.filter(email=email).exists():
                form.add_error('email', 'A user with this email already exists.')
            else:
                company_name = form.cleaned_data.get('company_name')
                company = Company.objects.create(name=company_name)
                director = form.save(commit=False)
                director.set_password(form.cleaned_data.get('password1'))
                director.role = 'company_admin'
                director.company = company
                director.save()
                company.director = director
                company.save()
                return redirect('/accounts/login')
    else:
        form = DirectorSignUpForm()
    return render(request, 'director_signup.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('/')  # already logged in

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                if user.role == 'company_admin':
                    return redirect('/')
                elif user.role == 'manager':
                    return redirect('/')
                elif user.role == 'employee':
                    return redirect('/')
                else:
                    return redirect('/')  # fallback
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('/accounts/login')

@login_required
def add_user(request):
    if request.user.role != 'company_admin':
        return redirect('/')  # only directors can add users
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            # Check if email already exists
            if CustomUser.objects.filter(email=email).exists():
                form.add_error('email', 'A user with this email already exists.')
            else:
                user = form.save(commit=False)
                user.company = request.user.company
                # Generate random password
                password = secrets.token_urlsafe(12)
                user.set_password(password)
                user.save()
                # Send email
                company_name = user.company.name if user.company else "the company"
                send_mail(
                    'Your Account Has Been Created',
                    f'Hello {user.name},\n\nYour account for {company_name} has been created.\n\nEmail: {user.email}\nPassword: {password}\n\nPlease login and change your password.',
                    'noreply@expensemanagement.com',
                    [user.email],
                    fail_silently=False,
                )
                return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'add_user.html', {'form': form})
    