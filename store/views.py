from django.shortcuts import render
from .models import Category, Customer, Product, Order
# Create your views here.

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})