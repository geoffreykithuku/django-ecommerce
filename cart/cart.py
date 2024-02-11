from store.models import Product

class Cart():
    def __init__(self, request):
        self.session = request.session 

        cart = self.session.get('session_key')

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
        self.cart = cart

    def add(self, product, qty):
        product_id = str(product.id)
        product_qty = qty

        if product_id in self.cart:
            pass 
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

    
    def __len__(self):
        return len(self.cart)
    
    
    def get_products(self):
        # get ids from cart
        product_ids = self.cart.keys()

        # use ids to lookup products from the database
        products = Product.objects.filter(id__in=product_ids)
        return products
    
    def get_quantities(self):
        quantities = self.cart
        return quantities   
    
    def update(self, product, qty):
        product_id = str(product.id)
        product_qty = int(qty)

        # get cart
        cart = self.cart

        # update the quantity
        cart[product_id] = product_qty

        # save the cart
        self.session.modified = True

        cart = self.cart
        return cart
    
    def delete(self, product):
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            self.session.modified = True
        else:
            pass
        return self.cart