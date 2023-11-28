def product_filter(request):
    filter_string = {}
    filter_mappings = {
        'search': 'name__icontains',
        'category': 'category__slug'
    }
    for key in request.GET:
        if request.GET.get(key):
            filter_string[filter_mappings[key]] = request.GET.get(key)

    return filter_string


class CartHandler(object):
    def __init__(self, cart_model):
        self.cart = cart_model

    def add_to_cart(self, product, quantity, request_user):
        cart, created = self.cart.objects.get_or_create(
            user=request_user, product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            cart.quantity += quantity
            cart.save()

        return cart

    def increment_cart(self, cart_id):
        cart = self.cart.objects.get(id=cart_id)
        cart.quantity += 1
        cart.save()

    def decrement_cart(self, cart_id):
        cart = self.cart.objects.get(id=cart_id)
        if cart.quantity > 1:
            cart.quantity -= 1
            cart.save()

    def modify_cart_quantity(self, cart_id, quantity):
        cart = self.cart.objects.get(id=cart_id)
        cart.quantity = quantity
        cart.save()

    def delete_cart_item(self, cart_id):
        cart = self.cart.objects.get(id=cart_id)
        cart.delete()
