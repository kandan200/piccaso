from django.shortcuts import render
from app.models import ArtworkCart, PublicEventCart, PrivateEventCart, Order, ArtworkOrderItem, PrivateEventOrderItem, PublicEventOrderItem
from django.shortcuts import get_object_or_404, render, get_list_or_404
from datetime import date
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from rest_framework import viewsets, authentication, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser


# Create your views here.
def cart(request):
    if request.user.is_authenticated:
        if ArtworkCart.objects.prefetch_related('user').filter(user=request.user).exists():
            artwork_cart_items = get_list_or_404(ArtworkCart, user=request.user)
        if PrivateEventCart.objects.prefetch_related('user').filter(user=request.user).exists():
            private_event_cart_items = get_list_or_404(PrivateEventCart, user=request.user)
        if PublicEventCart.objects.prefetch_related('user').filter(user=request.user).exists():
            public_event_cart_items = get_list_or_404(PublicEventCart, user=request.user)
        count = len(artwork_cart_items) + len(private_event_cart_items) + len(public_event_cart_items)
        return render(request, 'cart.html', {'artworks':artwork_cart_items, 'private_events_cart':private_event_cart_items, 'public_events_cart':public_event_cart_items, 'count':count}, status=200)
    else:
        message = "To create this cart, you need to either log into your account or create an account with us"
        return render (request, 'account.html', {'message':message}, status=401)

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
            return render(request, 'order.html', {'order':order, 'count':order_items}, status=200)    
        else:
            message = "To creaye this order, you need to either log into your account or create an account with us"
            return render (request, 'account.html', {'message':message}, status=401)

def payment_view(request, pk):
    if request.user.is_authenticated:
        return render(request, 'payment.html', {'pk':pk}, status=200) 
    else:
        message = "To proceed with this payment, you need to either log into your account or create an account with us"
        return render (request, 'account.html', {'message':message}, status=401)
     
def logout_view(request):
    logout(request)
    return redirect(reverse_lazy('home'), status=200)