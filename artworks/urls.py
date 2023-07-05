from django.urls import path
from . import views

urlpatterns = [
    path('artwork-to-cart/<int:pk>/', views.add_artwork_to_cart, name='add-artwork-to-cart'),
    path('artworks-list/', views.artwork_list_view, name='artworks-list'),
    path('artwork/<int:pk>/', views.artwork_view, name='artwork'),
    path('edit-artwork-order-item/<int:pk>/', views.edit_artwork_order_item, name="edit-artwork-order-item"),
  
]