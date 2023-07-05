from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'orders', views.OrderView, basename='orders')

urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('payment/<int:pk>/', views.payment_view, name='payment-view'),
    path('logout/', views.logout_view, name='logout'),
]

urlpatterns += router.urls
