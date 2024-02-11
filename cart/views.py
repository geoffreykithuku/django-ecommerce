from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse

# Create your views here.
def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_products()
    quantities = cart.get_quantities()
    return render(request, 'cart_summary.html', {'cart_products': cart_products,
                                                 'quantities': quantities})

def cart_add(request):
    #get cart
    cart = Cart(request)

    #test the POST
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))

        # get product quantity
        product_qty = int(request.POST.get('product_qty'))
        
        #look up for the product
        product = get_object_or_404(Product, id=product_id)

        #add to cart
        cart.add(product=product, qty=product_qty)

        #get cart qtty
        cart_quantity = cart.__len__()
        # response = JsonResponse({'Product Name:' : product.name})

        response = JsonResponse({'qty': cart_quantity})
        return response
    




def cart_delete(request):
    pass

def cart_update(request):
    pass