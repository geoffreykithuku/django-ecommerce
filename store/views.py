from django.shortcuts import render, redirect
from .models import Category, Customer, Product, Order, Profile

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserProfileUpdateForm
from django.db.models import Q


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

            #get user profile
            current_user = Profile.objects.get(user__id=request.user.id)

            # get saved cart from session
            

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
                messages.success(request, "Account created. Please fill in profile details")
                return redirect('update_info')
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


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, "User has been updated successfuly")
            return redirect('home')
        return render(request, 'update_user.html', {'user_form': user_form})
    else:
        messages.error(request, "You need to be logged in to update your profile")
        return redirect('login')
    

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user

        # check if user filled the form
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)

            # check if form is valid
            if form.is_valid():
                form.save()
                messages.success(request, "Password has been updated successfuly.")
                login(request, current_user)
                return redirect('update_user')
              
            else:
                for error in form.errors.values():
                    messages.error(request, error)
                return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {
                'form': form
            })
    else:
        messages.error(request, "You need to be logged in to update your password")
        return redirect('login')





    

def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)

        # check if user filled the form
        if request.method == 'POST':
            form = UserProfileUpdateForm(request.POST or None, instance=current_user)

            # check if form is valid
            if form.is_valid():
                form.save()
                messages.success(request, "Profile has been updated successfuly.")
                login(request, current_user.user)
                return redirect('home')
              
            else:
                for error in form.errors.values():
                    messages.error(request, error)
                return redirect('update_password')
        else:
            form = UserProfileUpdateForm(instance=current_user)
            return render(request, 'user_info.html', {
                'form': form
            })
    else:
        messages.error(request, "You need to be logged in to update your profile")
        return redirect('login')
    

def search(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        products = Product.objects.filter(Q(name__icontains=search) | Q(description__icontains=search))
        if not products:
            messages.error(request, "No products found")
            return render(request, 'search.html', {})
        else:
            return render(request, 'search.html', {'products': products, 'search': search})
        
   
       
    return render(request, 'search.html', {})