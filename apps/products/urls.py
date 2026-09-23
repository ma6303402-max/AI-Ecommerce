from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductCatalogView.as_view(), name='catalog'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='detail'),
    path('api/search/', views.product_search_api, name='search_api'),
]
