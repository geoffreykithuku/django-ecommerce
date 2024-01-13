from django.shortcuts import render
from .models import Category, Customer, Product, Order

from django.contrib.auth import authenticate, login, logout

# Create your views here.

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def about(request):
    products = Product.objects.all()
    return render(request, 'about.html', {'products': products})

def login_user(request):
    return render(request, 'login.html')

def logout_user(request):
    return render(request, 'logout.html')