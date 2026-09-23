from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('', include('apps.products.urls', namespace='products')),
    path('auth/', include('apps.authentication.urls', namespace='auth')),
    path('cart/', include('apps.cart.urls', namespace='cart')),
    path('orders/', include('apps.orders.urls', namespace='orders')),
    path('ai-recommendations/', include('apps.recommendations.urls', namespace='recommendations')),
    path('admin-dashboard/', include('apps.admin_dashboard.urls', namespace='admin_dashboard')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
