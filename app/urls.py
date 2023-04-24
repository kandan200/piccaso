from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'artwork-orders', views.ArtworkOrdersViewset)
router.register(r'public-event-orders', views.PublicEventOrdersViewset)
router.register(r'private-event-orders', views.PrivateEventOrdersViewset)


urlpatterns =[
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about-us'),
    path('contact-us/', views.contact_us, name='contact-us'),
    path('sign-in/', views.SignInFormView.as_view(), name='sign-in'),
    path('sign-up/', views.SignUpFormView.as_view(), name='sign-up'),
    path('book-public-event/', views.book_public_event, name='book-public-event'),
    path('boon-private-event/', views.book_private_event, name='book-private-event'),
    path('gallery/', views.gallery, name='gallery'),
    path('gallery-item/<int:pk>/', views.gallery_item, name='gallery-item'),
    path('past-events/', views.past_events_view, name='past-events'),
    path('event-gallery/<int:pk>/', views.event_gallery_view, name='event-gallery'),
    #url mapping for a view to display each item in an event gallery
    path('artists-list/', views.artists_list, name='artist-list'),
    path('artist/<int:pk>/', views.artist_view, name='artist'),
    path('artist-artworks/<int:pk1>/<int:pk2>/', views.artist_artwork_view, name='artist-artwork'),
]

urlpatterns += router.urls
