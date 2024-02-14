from django.shortcuts import render, redirect
from .models import Category, Customer, Product, Order

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm

# Create your views here.

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def about(request):
    products = Product.objects.all()
    return render(request, 'about.html', {'products': products})

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in")
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials. Please try again")
            return redirect('login')
    else:
        return render(request, 'login.html')

def logout_user(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password1')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You have signed up successfully")
                return redirect('home')
        else:
            messages.error(request,"An error occurred. Please try again.")
            return redirect('register')
    else:
        return render(request, 'register.html', {"form": form})
    
def product(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'product.html', {'product': product})

def category(request, slug):
    slug = slug.replace('-', ' ')
    try:
        category = Category.objects.get(name=slug)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products': products, 'category': category})

    except:
        messages.error(request, "That category does not exist.")
        return redirect('home')
    

def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {'categories': categories}) 
