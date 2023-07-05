from django.urls import path
from . import views


urlpatterns =[
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about-us'),
    path('contact-us/', views.contact_us, name='contact-us'),
    path('sign-in/', views.signin, name='sign-in'),
    path('sign-up/', views.signup, name='sign-up'),
    path('logout/', views.logout, name='signout'),
    path('reset-password/', views.password_reset, name='password-reset'),
    path('auth/users/activation/{uid}/{token}/', views.activation, name='activation'),
    path('auth/users/password/reset/confirm/{uid}/{token}/', views.password_reset_confirm, name='password-reset-confirm'),
]

