from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register(r'artwork-orders', views.ArtworkOrdersViewset)
# router.register(r'public-event-orders', views.PublicEventOrdersViewset)
# router.register(r'private-event-orders', views.PrivateEventOrdersViewset)
router.register(r'orders', views.OrderView, basename='orders')



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
    path('artworks-list/', views.artwork_list_view, name='artworks-list'),
    path('artwork-to-cart/', views.add_artwork_to_cart, name='add-artwork-to-cart'),
    path('cart/', views.cart, name='cart'),
    path('edit-private-event-order-item/<int:pk>/', views.edit_private_event_order, name='edit-private-event-order'),
    path('edit-public-event-order-item/<int:pk>/', views.edit_public_event_order, name='edit-public-event-order'),
    path('edit-artwork-order-item/<int:pk>/', views.edit_artwork_order_item, name="edit-artwork-order-item"),
    path('payment/<int:pk>/', views.payment_view, name='payment-view'),
]

urlpatterns += router.urls
