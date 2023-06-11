from django.urls import path
from .views import *

app_name = 'giftweb'

urlpatterns = [
    path('', home, name='home'),
    path('premium_home', premium_home, name='premium_home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('blogs/', blog_list, name='blog_list'),
    path('cart/', cart, name='cart'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),

    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('make_payment/<str:model_name>/<int:product_id>/', make_payment, name='make_payment'),
    path('payment_success/', payment_success, name='payment_success'),
    path('premium_product/<int:pk>/', PremiumProductDetailView.as_view(), name='premium_product_detail'),
    
    # Add the following URL for payment history
    path('payment_history/', payment_history, name='payment_history'),
]
