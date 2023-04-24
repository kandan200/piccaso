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
from .forms import PublicEventBookingForm, PrivateEventBookingForm, SignUpForm, SignInForm
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

                user = User(first_name=first_name, last_name=last_name, username=username, email=email,password=password)
                user.save()

                # Welcome Email
                subject = "Welcome to Piccaso"
                message = "Hello " + first_name + "!! \n" + "Welcome to Piccaso!! \nThank you for creating an account with us\n. We will send you a confirmation email, please confirm your email address. \n\nThanking You\n Kanu C. O"        
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
    form = PublicEventBookingForm()
    
    if request.method == "POST":
        form = PublicEventBookingForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'succesful_public_event_booking.html')
        
def book_private_event(request):
    form = PrivateEventBookingForm()
    
    if request.method == 'POST':
        form = PrivateEventBookingForm(request.POST)
        if form.is_valid():
            form.save()
            event = PrivateEvent.objects.get(title=form.cleaned_data['title'])
            user = request.user
            private_event_cart = PrivateEventCart(user=user, event =event)
            private_event_cart.save()
            return render(request, 'succesful_private_event_booking', {'event':event})

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
    return render(request, 'event_gallery.html', {'images':event_gallery})

def artists_list(request):
    list = Artist.objects.all()
    return render(request, 'artists_list.html', {'list':list})

def artist_view(request, pk):
    artist = Artist.objects.get(pk=pk)
    artworks = get_list_or_404(Artwork, artist=artist)
    return render(request, 'artist.html', {'artist':artist, 'artworks':artworks})

def artist_artwork_view(request, pk1, pk2):
    artist = Artist.objects.get(pk=pk1)
    artwork = artist.artwork_set.get(pk=pk2)
    return render(request, 'artist_artwork.html', {'artwork':artwork})

class ArtworkOrdersViewset(viewsets.ModelViewSet):
    queryset = ArtworkOrderItem.objects.all()
    # template_name = 'artwork_order_items.html'
    # permission_classes =[IsAuthenticated]
    # ordering_fields =['user','delivery_crew','status','date']
    # search_fields = ['delivery_crew__username', 'user__username', 'featured']

    def list(self, request):
        order_items = self.queryset.filter(order__user=request.user)
        return render(request, 'artwork_order_items.html', {'order':order_items})
        
    def create(self, request):
        user=request.user
        cart = list(ArtworkCart.objects.filter(user=user))
        total = 0
        daate = date.today()
        order = Order(user=user, total=total, date=daate)
        order.save()
        artwork_order_items = []
        for artwork in cart:
            price = artwork.price 
            item = artwork.item
            artwork_order_item = ArtworkOrderItem(order=order, item=item, price=price)
            artwork_order_item.save()
            order.total += price
            order.save()
            artwork_order_items.append(artwork_order_item)
            artwork.delete()
        return render(request, 'artwork_order_items.html', {'order':artwork_order_items})

    def retrieve(self, request, pk):
            order = Order.objects.get(pk=pk)
            if order.user == request.user:
                order_items = get_list_or_404(ArtworkOrderItem, order=order)
                return render(request, 'artwork_order_items.html', {'order':order_items})
            else:
                messages.error(request, 'you cant view this order because it belongs to another user')
                #wire up this url
                return HttpResponseRedirect(reverse_lazy('home'))
            
    #dependency - view will be called from an edit-order-item view-template form, the form method will be PUT and the payload will be the form data
    def destroy(self, request, pk):
        order_item = get_object_or_404(ArtworkOrderItem, pk=pk)
        order_item.delete()
        messages.success(request, 'Item succesfully deleted')
                        #wire up this url to return to the retrive method of this same viewset7'        
        return HttpResponseRedirect(reverse_lazy('home'))


class PublicEventOrdersViewset(viewsets.ModelViewSet):
    queryset = PublicEventOrderItem.objects.all()
    # permission_classes =[IsAuthenticated]
    # ordering_fields =['user','delivery_crew','status','date']
    # search_fields = ['delivery_crew__username', 'user__username', 'featured']

    def list(self, request):
        order_items = self.queryset.filter(order__user=request.user)
        return render(request, 'public_event_order_items.html', {'order':order_items})
    
    #this view will be called from ----- wire it up
    def create(self, request):
        user=request.user
        cart = PublicEventCart.objects.filter(user=user)
        total = 0
        daate = date.today()
        order = Order(user=user, total=total, date=daate)
        order.save()
        public_event_order_items = []
        for item in cart:
            event = item.event
            number_of_tickets = item.number_of_tickets
            unit_price = item.unit_price
            price = unit_price * number_of_tickets
            public_event_order_item = PublicEventOrderItem(order=order, event=event, price=price, unit_price=unit_price, number_of_tickets=number_of_tickets)
            public_event_order_item.save()
            order.total += price
            order.save()
            public_event_order_items.append(public_event_order_item)
            item.delete()
        return render(request, 'public_event_order_items.html', {'order':public_event_order_items})
    
    def retrieve(self, request, pk):
            order = Order.objects.get(pk=pk)
            if order.user == request.user:
                order_items = get_list_or_404(PublicEventOrderItem, order=order)
                return render(request, 'public_event_order_items.html', {'order':order_items})
            else:
                messages.error(request, 'you cant view this order because it belongs to another user')
                #wire up this url
                return HttpResponseRedirect(reverse_lazy('home'))
            
       #wire up this view in relation to the view from which it will be called     
    def partial_update(self, request, pk):
        order_item = PublicEventOrderItem.objects.get(pk=pk)
        order_item.order = request.data['order']
        order_item.event = request.data['event']
        # order_item.unit_price = request.data['unit_price']
        order_item.number_of_tickets = request.data['number_of_tickets']
        order_item.price = order_item.unit_price * order_item.number_of_tickets
        order_item.save()
        return render(request, 'public_event_order_items.html', {'order':order_item})
        
           
    #dependency - view will be called from an edit-order-item view-template form, the form method will be PUT and the payload will be the form data
    def destroy(self, request, pk):
        order_item = get_object_or_404(PublicEventOrderItem, pk=pk)
        order_item.delete()
        messages.success(request, 'Item succesfully deleted')
                        #wire up this url to return to the retrive method of this same viewset7'        
        return HttpResponseRedirect(reverse_lazy('home'))


class PrivateEventOrdersViewset(viewsets.ModelViewSet):
    queryset = PrivateEventOrderItem.objects.all()
    # permission_classes =[IsAuthenticated]
    # ordering_fields =['user','delivery_crew','status','date']
    # search_fields = ['delivery_crew__username', 'user__username', 'featured']

    def list(self, request):
        order_items = self.queryset.filter(order__user=request.user)
        return render(request, 'private_event_order_items.html', {'order':order_items})
    
    #this view will be called from ----- wire it up
    def create(self, request):
        user=request.user
        cart = PrivateEventCart.objects.filter(user=user)
        total = 0
        daate = date.today()
        order = Order(user=user, total=total, date=daate)
        order.save()
        private_event_order_items = []
        for item in cart:
            event = item.event
            private_event_order_item = PrivateEventOrderItem(order=order, event=event)
            private_event_order_item.save()
            #find a way to include the price in the template
            order.save()
            private_event_order_items.append(private_event_order_item)
            item.delete()
        return render(request, 'private_event_order_items.html', {'order':private_event_order_items})
    
    def retrieve(self, request, pk):
            order = Order.objects.get(pk=pk)
            if order.user == request.user:
                order_items = get_list_or_404(PrivateEventOrderItem, order=order)
                return render(request, 'private_event_order_items.html', {'order':order_items})
            else:
                messages.error(request, 'you cant view this order because it belongs to another user')
                #wire up this url
                return HttpResponseRedirect(reverse_lazy('home'))
            
       #wire up this view in relation to the view from which it will be called     
    def partial_update(self, request, pk):
        order_item = PrivateEventOrderItem.objects.get(pk=pk)
        order_item.order = request.data['order']
        order_item.event.date = request.data['event']['date']
        order_item.event.venue = request.data['event']['venue']
        order_item.event.number_of_persons = request.data['event']['number_of_persons']
        order_item.event.contact = request.data['event']['contact']
        order_item.event.email = request.data['event']['email']
        
        # order_item.unit_price = request.data['unit_price']
        order_item.save()
        return render(request, 'public_event_order_items.html', {'order':order_item})
                  
    #dependency - view will be called from an edit-order-item view-template form, the form method will be PUT and the payload will be the form data
    def destroy(self, request, pk):
        order_item = get_object_or_404(PublicEventOrderItem, pk=pk)
        order_item.delete()
        messages.success(request, 'Item succesfully deleted')
        
        #wire up this url to return to the retrive method of this same viewset7'        
        return HttpResponseRedirect(reverse_lazy('home'))
