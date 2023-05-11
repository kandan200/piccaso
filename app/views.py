from django.shortcuts import render
from decimal import Decimal
from django.urls import reverse, reverse_lazy
import random
from django.forms import ValidationError, model_to_dict
from django.shortcuts import get_list_or_404, get_object_or_404, render
from .models import Artwork, PublicEvent, PrivateEvent, PublicEventCart, PrivateEventCart, Artist, EventImage, ArtworkCart, ArtworkOrderItem, PublicEventOrderItem, PrivateEventOrderItem, Order
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.models import User, Group
import bleach
from datetime import date
from django.core import serializers
from .forms import PublicEventBookingForm, PrivateEventBookingForm, SignUpForm, SignInForm, EditPublicEventOrderItemForm, EditArtworkOrderItemForm
import json
from django.views.generic.edit import FormView, UpdateView, DeleteView, ModelFormMixin
from django.core.mail import EmailMessage, send_mail
from project import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets, authentication, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser



# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact_us(request):
    return render(request, 'contact_us.html')

class SignInFormView(FormView):
    template_name = 'sign_in.html'
    form_class = SignInForm

    def get(self, request):
        form = SignInForm()
        return render(request, 'sign_in.html', {'form': form})

    def post(self, request):
        form = SignInForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have succesfully logged in')
            #wire up the url
            return HttpResponseRedirect(reverse_lazy('home'))
        else:
            messages.error(request, 'Bad Login credentials')
            return HttpResponseRedirect(reverse_lazy('sign_in'))


class SignUpFormView(FormView):
    # i can use CreateView generic view to implement this view too
    template_name = 'sign_up.html'
    form_class = SignUpForm
 # explore use of success_url attribute as a way to redirect after succesful saving of object to the model 

    def get(self, request):
        form = SignUpForm()
        return render(request, 'sign_up.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)

        if request.POST['password'] == request.POST['confirm_password']:
            if form.is_valid():
                last_name = form.cleaned_data['last_name'] 
                password = form.cleaned_data['password']   
                email = form.cleaned_data['email']
                first_name = form.cleaned_data['first_name']
                username = form.cleaned_data['username']
                form.save()
                #Aunthenticate the form manually before saving the form and creating user object
                User.objects.create(first_name=first_name, last_name=last_name, username=username, email=email,password=password)

                # Welcome Email
                subject = "Welcome to Piccaso"
                message = "Hello " + first_name + "!! \n" + "Welcome to Piccaso!! \nThank you for creating an account with us\n. We will send you a confirmation email, please confirm your email address. \n\nThank You\n Kanu C. O"        
                from_email = settings.EMAIL_HOST_USER
                to_list = [email]
                send_mail(subject, message, from_email, to_list, fail_silently=True)
        
                login_user = authenticate(username=username, password=password)
                login(request, login_user)

                messages.success(request, 'You have succesfully created, saved, and logged in the user')
                #fix url for next line
                return HttpResponseRedirect(reverse_lazy('home'))

            else:
                return render(request, 'sign_up.html', {'form': form})
        else:
            messages.error(request, 'Password and Confirm Password do not match')
            #implement form validation for password/confirm_password symmetry
            return render(request, 'sign_up.html', {'form':form})

def book_public_event(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            form = PublicEventBookingForm()
            return render(request, 'book_public_event.html', {'form':form})
        else:
            return render (request, 'account.html', {})
 
    if request.method == "POST":
        if request.user.is_authenticated:
            form = PublicEventBookingForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "You have succesfully added event to cart.")
                return HttpResponseRedirect(reverse_lazy('home'))
            #instead of redirecting to home, consider implementing a front end js event to load the succesful message after setting up account 
        else:
            messages.error(request, 'You need an account to perform this task')
            return render (request, 'account.html', {})


def book_private_event(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            form = PrivateEventBookingForm()
            return render(request, 'book_private_event.html', {'form':form})
        else:
            messages.error(request, 'You need an account to perform this task')
            return render (request, 'account.html', {})

    
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = PrivateEventBookingForm(request.POST)
            if form.is_valid():
                form.save()
                event = PrivateEvent.objects.get(title=form.cleaned_data['title'])
                user = request.user
                PrivateEventCart.objects.create(user=user, event=event)
                messages.success(request, "You have succesfully added event to cart")
                return HttpResponseRedirect(reverse_lazy('home'))
        else:
            messages.error(request, 'You need an account to perform this task')
            return render (request, 'account.html', {})

def add_artwork_to_cart(request, pk):
    if request.user.is_authenticated:
        artwork = Artwork.objects.get()
        ArtworkCart.objects.create(item=artwork, user=request.user)
        messages.success(request, "You have added item to the cart")
        return HttpResponseRedirect(reverse_lazy('artworks-list'))
    else:
        messages.error(request, 'You need an account to perform this task')
        return render (request, 'account.html', {})

       
def gallery(request):
    items = EventImage.objects.all()
    return render(request, 'gallery.html', {'items':items})

def gallery_item(request, pk):
    item = EventImage.objects.get(pk=pk)
    return render(request, 'gallery_item.html', {'item':item})

def past_events_view(request):
    events = PublicEvent.objects.all()
    return render(request, 'past_events.html', {'events':events})

def event_gallery_view(request, pk):
    event = PublicEvent.objects.get(pk=pk)
    event_gallery = get_list_or_404(EventImage, event=event)
    return render(request, 'event_gallery.html', {'images':event_gallery, 'event':event})

def artwork_list_view(request):
    artworks = Artwork.objects.all()
    return render(request, 'artworks.html', {'artworks':artworks})    

def artwork_view(request, pk):
    artwork = Artwork.objects.get(pk=pk)
    return render(request, 'artwork.html', {'artwork':artwork})    


def cart(request):
    if request.user.is_authenticated:
        if ArtworkCart.objects.prefetch_related('user').filter(user=request.user).exists():
            artwork_cart_items = get_list_or_404(ArtworkCart, user=request.user)
        if PrivateEventCart.objects.prefetch_related('user').filter(user=request.user).exists():
            private_event_cart_items = get_list_or_404(PrivateEventCart, user=request.user)
        if PublicEventCart.objects.prefetch_related('user').filter(user=request.user).exists():
            public_event_cart_items = get_list_or_404(PublicEventCart, user=request.user)
        count = len(artwork_cart_items) + len(private_event_cart_items) + len(public_event_cart_items)
        return render(request, 'cart.html', {'artworks':artwork_cart_items, 'private_events_cart':private_event_cart_items, 'public_events_cart':public_event_cart_items, 'count':count})
    else:
        messages.error(request, 'You need an account to perform this task')
        return render (request, 'account.html', {})


#consider serilizers instad of forms to allow readonly
def edit_private_event_order(request, pk):
    if request.method == 'GET':
        if request.user.is_authenticated:
            event_cart = get_object_or_404(PrivateEventCart, pk=pk)
            form = PrivateEventBookingForm(instance=event_cart.event)
            event_pk = event_cart.event.pk
            return render(request, 'edit_private_event.html', {'form':form, 'pk':event_pk})
        else:
            messages.error(request, 'You need an account to perform this task')
            return render (request, 'account.html', {})

    if request.method == 'POST':
        if request.user.is_authenticated:
            instance = PrivateEvent.objects.get(pk=pk)
            form = PrivateEventBookingForm(request.POST, instance=instance)
            if form.is_valid():
                instance.title = form.validated_data['title']
                instance.date = form.validated_data['date']
                instance.venue = form.validated_data['venue']
                instance.number_of_persons = form.validated_data['number_of_persons']
                instance.contact = form.validated_data['contact']
                instance.email = form.validated_data['email']
                instance.save()
            return HttpResponseRedirect(reverse_lazy('cart'))
        else:
            messages.error(request, 'You need an account to perform this task')
            return render (request, 'account.html', {})


    if request.method == 'DELETE':
        if request.user.is_authenticated:
            cart_item = get_object_or_404(PrivateEventCart, pk=pk)
            cart_item.delete()
            return HttpResponseRedirect(reverse_lazy('cart'))
        else:
            messages.error(request, 'You need an account to perform this task')
            return render (request, 'account.html', {})


def edit_public_event_order(request, pk):
    if request.method == 'GET':
        if request.user.is_authenticated:
            event_cart = get_object_or_404(PublicEventCart, pk=pk)
            form = EditPublicEventOrderItemForm(instance=event_cart)
            return render(request, 'edit_public_event.html', {'form':form, 'pk':pk})
        else:
            messages.error(request, 'You need an account to perform this task')
            return render (request, 'account.html', {})

    if request.method == 'POST':
        if request.user.is_authenticated:
            instance = get_object_or_404(PublicEventCart, pk=pk)
            form = PublicEventBookingForm(request.POST, instance=instance)
            if form.is_valid():
                instance.number_of_tickets = form.validated_data['number_of_tickets']
                instance.save()
            return HttpResponseRedirect(reverse_lazy('cart'))
        else:
            messages.error(request, 'You need an account to perform this task')
            return render (request, 'account.html', {})

    if request.method == 'DELETE':
        if request.user.is_authenticated:
            cart_item = get_object_or_404(PublicEventCart, pk=pk)
            cart_item.delete()
            return HttpResponseRedirect(reverse_lazy('cart'))
        else:
            messages.error(request, 'You need an account to perform this task')
            return render (request, 'account.html', {})



def edit_artwork_order_item(request, pk):
    if request.method == 'DELETE':
        if request.user.is_authenticated:
            cart_item = get_object_or_404(ArtworkCart, pk=pk)
            cart_item.delete()
            return HttpResponseRedirect(reverse_lazy('cart'))
        else:
            messages.error(request, 'You need an account to perform this task')
            return render (request, 'account.html', {})


class OrderView(viewsets.ViewSet):
    def create(self, request):
        user = request.user
        if user.is_authenticated:
            order = Order.objects.create(user=user, total=0, date=date.today())    
            order_items = 0
            if ArtworkCart.objects.prefetch_related('user').filter(user=user).exists():
                for artwork in list(ArtworkCart.objects.filter(user=user)):
                    ArtworkOrderItem.objects.create(order=order, item=artwork.item, price=artwork.item.price)
                    order.total += artwork.item.price
                    order.save()
                    order_items += 1
                    artwork.delete()
                    
            if PublicEventCart.objects.prefetch_related('user').filter(user=user).exists():
                cart_item = get_object_or_404(PublicEventCart, user=user)
                PublicEventOrderItem.objects.create(order=order, event=cart_item.event, number_of_tickets=cart_item.number_of_tickets, unit_price=cart_item.unit_price, price=cart_item.price)
                order.total += cart_item.price
                order.save()
                order_items += 1
                cart_item.delete()

            if PrivateEventCart.objects.prefetch_related('user').filter(user=user).exists():
                for event in list(PrivateEventCart.objects.filter(user=user)):
                    PrivateEventOrderItem.objects.create(order=order, event=event.event)
                    order.total += (event.event.number_of_persons*15)
                    order.save()
                    order_items += 1
                    event.delete()        
            return render(request, 'order.html', {'order':order, 'count':order_items})    
        else:
            messages.error(request, 'You need an account to perform this task')
            return render (request, 'account.html', {})

def payment_view(request, pk):
    if request.user.is_authenticated:
        return render(request, 'payment.html', {'pk':pk}) 
    else:
        messages.error(request, 'You need an account to perform this task')
        return render (request, 'account.html', {})
     
