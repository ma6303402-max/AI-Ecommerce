from .models import Cart, CartItem
from apps.products.models import Product

def get_or_create_cart(request):
    """
    Helper function to fetch or create the Cart for a logged in user or guest session.
    Automatically merges guest cart into user cart upon login.
    """
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        # Check if guest session cart exists and merge
        session_key = request.session.session_key
        if session_key:
            guest_cart = Cart.objects.filter(session_key=session_key, user__isnull=True).first()
            if guest_cart:
                for item in guest_cart.items.all():
                    cart_item, item_created = CartItem.objects.get_or_create(
                        cart=cart,
                        product=item.product,
                        defaults={'quantity': item.quantity}
                    )
                    if not item_created:
                        cart_item.quantity += item.quantity
                        cart_item.save()
                guest_cart.delete()
        return cart
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key, user__isnull=True)
        return cart
