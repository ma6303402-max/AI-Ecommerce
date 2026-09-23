from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.contrib import messages
from apps.products.models import Product
from .models import CartItem
from .cart import get_or_create_cart
from apps.recommendations.engine import RecommendationEngine

class CartDetailView(View):
    def get(self, request):
        cart = get_or_create_cart(request)
        cart_items = cart.items.select_related('product').all()

        # Fetch personalized AI recommendations based on cart contents
        engine = RecommendationEngine()
        cart_recommendations = engine.get_personalized_recommendations(request, limit=3)

        context = {
            'cart': cart,
            'cart_items': cart_items,
            'cart_recommendations': cart_recommendations,
        }
        return render(request, 'cart/cart.html', context)

def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        quantity = int(request.POST.get('quantity', 1))

        if quantity > product.stock:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'Requested quantity exceeds available stock.'}, status=400)
            messages.error(request, 'Requested quantity exceeds available stock.')
            return redirect('products:detail', slug=product.slug)

        cart = get_or_create_cart(request)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity

        cart_item.save()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f"Added '{product.title}' to cart!",
                'cart_total_items': cart.get_total_items(),
                'cart_total_price': str(cart.get_total_price()),
            })

        messages.success(request, f"Added '{product.title}' to your shopping cart!")
        return redirect('cart:view_cart')

    return redirect('products:catalog')

def update_cart_item(request, item_id):
    if request.method == 'POST':
        cart = get_or_create_cart(request)
        cart_item = get_object_or_404(CartItem, pk=item_id, cart=cart)
        quantity = int(request.POST.get('quantity', 1))

        if quantity <= 0:
            cart_item.delete()
        elif quantity > cart_item.product.stock:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'Not enough stock available.'}, status=400)
            messages.error(request, 'Not enough stock available.')
            return redirect('cart:view_cart')
        else:
            cart_item.quantity = quantity
            cart_item.save()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'item_total': str(cart_item.get_total_price()) if quantity > 0 else '0.00',
                'cart_total_items': cart.get_total_items(),
                'cart_total_price': str(cart.get_total_price()),
            })

        return redirect('cart:view_cart')

    return redirect('cart:view_cart')

def remove_from_cart(request, item_id):
    if request.method == 'POST':
        cart = get_or_create_cart(request)
        cart_item = get_object_or_404(CartItem, pk=item_id, cart=cart)
        product_name = cart_item.product.title
        cart_item.delete()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f"Removed '{product_name}' from cart.",
                'cart_total_items': cart.get_total_items(),
                'cart_total_price': str(cart.get_total_price()),
            })

        messages.info(request, f"Removed '{product_name}' from cart.")
        return redirect('cart:view_cart')

    return redirect('cart:view_cart')
