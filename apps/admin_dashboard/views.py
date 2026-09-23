from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.db.models import Sum, Count
from django.contrib.auth.mixins import UserPassesTestMixin
from apps.products.models import Product, Category
from apps.products.forms import ProductForm
from apps.orders.models import Order
from apps.authentication.models import User

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and (self.request.user.is_staff or self.request.user.role == 'administrator')

class DashboardOverviewView(AdminRequiredMixin, View):
    def get(self, request):
        total_products = Product.objects.count()
        total_orders = Order.objects.count()
        total_revenue = Order.objects.aggregate(total=Sum('total_amount'))['total'] or 0
        if total_revenue:
            total_revenue = round(float(total_revenue), 2)
        total_customers = User.objects.filter(role='customer').count()

        recent_orders = Order.objects.select_related('user').all()[:5]
        products = Product.objects.select_related('category').all()[:10]

        context = {
            'total_products': total_products,
            'total_orders': total_orders,
            'total_revenue': total_revenue,
            'total_customers': total_customers,
            'recent_orders': recent_orders,
            'products': products,
        }
        return render(request, 'admin_dashboard/dashboard.html', context)

class ProductCreateView(AdminRequiredMixin, View):
    def get(self, request):
        form = ProductForm()
        return render(request, 'admin_dashboard/product_form.html', {'form': form, 'title': 'Add New Product'})

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            messages.success(request, f"Product '{product.title}' created successfully!")
            return redirect('admin_dashboard:overview')
        return render(request, 'admin_dashboard/product_form.html', {'form': form, 'title': 'Add New Product'})

class ProductUpdateView(AdminRequiredMixin, View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = ProductForm(instance=product)
        return render(request, 'admin_dashboard/product_form.html', {'form': form, 'title': f'Edit Product #{pk}', 'product': product})

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f"Product '{product.title}' updated successfully!")
            return redirect('admin_dashboard:overview')
        return render(request, 'admin_dashboard/product_form.html', {'form': form, 'title': f'Edit Product #{pk}', 'product': product})

class ProductDeleteView(AdminRequiredMixin, View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        title = product.title
        product.delete()
        messages.info(request, f"Product '{title}' deleted.")
        return redirect('admin_dashboard:overview')

class OrderStatusUpdateView(AdminRequiredMixin, View):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, f"Order #{order.get_order_number()} status updated to {order.get_status_display()}.")
        return redirect('admin_dashboard:overview')
