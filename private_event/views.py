from django.shortcuts import render
from app.models import PrivateEvent, PrivateEventCart
from app.forms import PrivateEventBookingForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect


# Create your views here.
def book_private_event(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            form = PrivateEventBookingForm()
            return render(request, 'book_private_event.html', {'form':form}, status=200)
        else:
            message = "To book this exclusive event, you need to either log into your account or create an account with us"
            return render (request, 'account.html', {'message':message}, status=401)

    
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = PrivateEventBookingForm(request.POST)
            if form.is_valid():
                form.save()
                event = PrivateEvent.objects.get(title=form.cleaned_data['title'])
                user = request.user
                PrivateEventCart.objects.create(user=user, event=event)
                return redirect(reverse_lazy('home'), status=302)
            else:
                message = 'There were some errors in the submited date'
                return render(request, 'book_private_event.html', {'form':form, 'message':message}, status=400)
        else:
            message = "To book this exclusive event, you need to either log into your account or create an account with us"
            return render (request, 'account.html', {'message':message}, status=401)

#consider serilizers instad of forms to allow readonly
def edit_private_event_order(request, pk):
    if request.method == 'GET':
        if request.user.is_authenticated:
            event_cart = get_object_or_404(PrivateEventCart, pk=pk)
            form = PrivateEventBookingForm(instance=event_cart.event)
            event_pk = event_cart.event.pk
            return render(request, 'edit_private_event.html', {'form':form, 'pk':event_pk}, status=200)
        else:
            message = "To edit this exclusive event, you need to either log into your account or create an account with us"
            return render (request, 'account.html', {'message':message}, status=401)

    if request.method == 'PUT':
        if request.user.is_authenticated:
            instance = PrivateEvent.objects.get(pk=pk)
            instance.title = request.PUT['title']
            instance.date = request.PUT['date']
            instance.venue = request.PUT['venue']
            instance.number_of_persons = request.PUT['number_of_persons']
            instance.contact = request.PUT['contact']
            instance.email = request.PUT['email']
            instance.save()
            return redirect(reverse_lazy('cart'), status=302)
        else:
            message = "To edit this exclusive event, you need to either log into your account or create an account with us"
            return render (request, 'account.html', {'message':message}, status=401)


    if request.method == 'DELETE':
        if request.user.is_authenticated:
            cart_item = get_object_or_404(PrivateEventCart, pk=pk)
            cart_item.delete()
            return redirect(reverse_lazy('cart'), status=302)
        else:
            message = "To delete this exclusive event, you need to either log into your account or create an account with us"
            return render (request, 'account.html', {'message':message}, status=401)
