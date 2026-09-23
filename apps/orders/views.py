from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.cart.cart import get_or_create_cart
from .models import Order, OrderItem
from .forms import CheckoutForm

class CheckoutView(View):
    def get(self, request):
        cart = get_or_create_cart(request)
        if cart.items.count() == 0:
            messages.warning(request, "Your cart is empty. Add products before checking out!")
            return redirect('products:catalog')

        initial_data = {}
        if request.user.is_authenticated:
            initial_data['full_name'] = f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username
            initial_data['email'] = request.user.email

        form = CheckoutForm(initial=initial_data)
        context = {
            'form': form,
            'cart': cart,
            'cart_items': cart.items.all(),
        }
        return render(request, 'orders/checkout.html', context)

    def post(self, request):
        cart = get_or_create_cart(request)
        if cart.items.count() == 0:
            messages.warning(request, "Your cart is empty.")
            return redirect('products:catalog')

        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.total_amount = cart.get_total_price()
            order.status = 'PENDING'
            order.save()

            # Transfer cart items to OrderItems & update product stock
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    product_title=item.product.title,
                    price=item.product.price,
                    quantity=item.quantity
                )
                # Stock deduction
                if item.product.stock >= item.quantity:
                    item.product.stock -= item.quantity
                    item.product.save()

            # Clear cart
            cart.items.all().delete()

            messages.success(request, f"Order #{order.get_order_number()} placed successfully!")
            return redirect('orders:detail', order_id=order.id)

        return render(request, 'orders/checkout.html', {'form': form, 'cart': cart, 'cart_items': cart.items.all()})

class OrderHistoryView(LoginRequiredMixin, View):
    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        return render(request, 'orders/history.html', {'orders': orders})

class OrderDetailView(View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        # Security check: if order belongs to a user, verify access
        if order.user and request.user != order.user and not request.user.is_staff:
            messages.error(request, "You are not authorized to view this order.")
            return redirect('products:catalog')

        return render(request, 'orders/detail.html', {'order': order})
