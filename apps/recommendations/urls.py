from django.urls import path
from . import views

app_name = 'recommendations'

urlpatterns = [
    path('api/product/<int:product_id>/', views.get_recommendations_api, name='product_recommendations_api'),
    path('api/personalized/', views.personalized_recommendations_api, name='personalized_api'),
    path('api/chat/', views.ai_chat_recommendations_api, name='chat_api'),
]
