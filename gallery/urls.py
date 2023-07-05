from django.urls import path
from . import views

urlpatterns = [
    path('gallery/', views.gallery, name='gallery'),
    path('gallery-item/<int:pk>/', views.gallery_item, name='gallery-item'),
    path('past-events/', views.past_events_view, name='past-events'),
    path('event-gallery/<int:pk>/', views.event_gallery_view, name='event-gallery'),    
]