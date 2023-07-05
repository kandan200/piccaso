from django.urls import path
from . import views

urlpatterns = [
    path('book-private-event/', views.book_private_event, name='book-private-event'),
    path('edit-private-event-order-item/<int:pk>/', views.edit_private_event_order, name='edit-private-event-order'),    
]