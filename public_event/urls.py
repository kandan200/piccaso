from django.urls import path
from . import views

urlpatterns = [
    path('book-public-event/', views.book_public_event, name='book-public-event'),
    path('edit-public-event-order-item/<int:pk>/', views.edit_public_event_order, name='edit-public-event-order'),
]