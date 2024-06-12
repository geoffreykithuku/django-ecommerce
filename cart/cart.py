from store.models import Product, Profile

class Cart():
    def __init__(self, request):
        self.session = request.session 
        self.request = request

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

        # deal with logged in user
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)

            carty = str(self.cart)
            carty = carty.replace("\'", "\"")

            # save carty to profile model
            current_user.update(old_cart=str(carty))
            
    def db_add(self, product, qty):
         product_id = str(product)
         product_qty = qty

         if product_id in self.cart:
            pass 
         else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)

         self.session.modified = True

        # deal with logged in user
         if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)

            carty = str(self.cart)
            carty = carty.replace("\'", "\"")

            # save carty to profile model
            current_user.update(old_cart=str(carty))


    
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

        
         # deal with logged in user
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)

            carty = str(self.cart)
            carty = carty.replace("\'", "\"")

            # save carty to profile model
            current_user.update(old_cart=str(carty))
            
        cart = self.cart
        return cart
    
    def delete(self, product):
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

         # deal with logged in user
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)

            carty = str(self.cart)
            carty = carty.replace("\'", "\"")

            # save carty to profile model
            current_user.update(old_cart=str(carty))
        
    
    def cart_total(self):
        cart = self.cart
        total = 0
        for item in cart:
            product = Product.objects.get(id=item)
            if product.on_offer:
                total += (product.offer_price * cart[item])
            else:
                total += (product.price * cart[item])

        return total