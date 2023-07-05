from django.shortcuts import render
from app.models import PublicEventCart
from app.forms import PublicEventBookingForm, EditPublicEventOrderItemForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect

# Create your views here.
def book_public_event(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            form = PublicEventBookingForm()
            return render(request, 'book_public_event.html', {'form':form}, status=200)
        else:
            message = "To book this featured event, you need to either log into your account or create an account with us"
            return render (request, 'account.html', {'message':message}, status=401)
 
    if request.method == "POST":
        if request.user.is_authenticated:
            form = PublicEventBookingForm(request.POST)
            if form.is_valid():
                form.save()
                redirect(reverse_lazy('home'), status=302)
            else:
                message = 'There were some errors in the submited date'
                return render(request, 'book_public_event.html', {'form':form, 'message':message}, status=400)
            #instead of redirecting to home, consider implementing a front end js event to load the succesful message after setting up account 
        else:
            message = "To book this featured event, you need to either log into your account or create an account with us"
            return render (request, 'account.html', {'message':message}, status=401)

def edit_public_event_order(request, pk):
    if request.method == 'GET':
        if request.user.is_authenticated:
            event_cart = get_object_or_404(PublicEventCart, pk=pk)
            form = EditPublicEventOrderItemForm(instance=event_cart)
            return render(request, 'edit_public_event.html', {'form':form, 'pk':pk}, status=200)
        else:
            message = "To edit this exclusive event, you need to either log into your account or create an account with us"
            return render (request, 'account.html', {'message':message}, status=401)

    if request.method == 'PATCH':
        if request.user.is_authenticated:
            instance = get_object_or_404(PublicEventCart, pk=pk)
            instance.number_of_tickets = request.PATCH['number_of_tickets']
            instance.save()
            return redirect(reverse_lazy('cart'), status=302)
        else:
            message = "To book this exclusive event, you need to either log into your account or create an account with us"
            return render (request, 'account.html', {'message':message}, status=401)

    if request.method == 'DELETE':
        if request.user.is_authenticated:
            cart_item = get_object_or_404(PublicEventCart, pk=pk)
            cart_item.delete()
            return redirect(reverse_lazy('cart'), status=302)
        else:
            message = "To edit this exclusive event, you need to either log into your account or create an account with us"
            return render (request, 'account.html', {'message':message}, status=401)

