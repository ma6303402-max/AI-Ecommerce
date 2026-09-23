from .cart import get_or_create_cart

def cart_context(request):
    try:
        cart = get_or_create_cart(request)
        return {
            'cart': cart,
            'cart_total_items': cart.get_total_items(),
            'cart_total_price': cart.get_total_price(),
        }
    except Exception:
        return {
            'cart': None,
            'cart_total_items': 0,
            'cart_total_price': 0,
        }
