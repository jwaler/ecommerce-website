from django.urls import path, include
from django.contrib import admin
from django.urls import path
from . import views

# For IMG processing
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('pay/', views.payment, name="payment"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
