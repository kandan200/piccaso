from django.shortcuts import render
from app.models import Artwork, ArtworkCart
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect

# Create your views here.
def add_artwork_to_cart(request, pk):
    if request.user.is_authenticated:
        artwork = Artwork.objects.get(pk=pk)
        ArtworkCart.objects.create(item=artwork, user=request.user)
        return redirect(reverse_lazy('artworks-list'), status=302)
    else:
        message = "To book this exclusive event, you need to either log into your account or create an account with us"
        return render (request, 'account.html', {'message':message}, status=401)

def artwork_list_view(request):
    artworks = Artwork.objects.all()
    return render(request, 'artworks.html', {'artworks':artworks}, status=200)    

def artwork_view(request, pk):
    artwork = Artwork.objects.get(pk=pk)
    return render(request, 'artwork.html', {'artwork':artwork}, status=200)    

def edit_artwork_order_item(request, pk):
    if request.method == 'DELETE':
        if request.user.is_authenticated:
            cart_item = get_object_or_404(ArtworkCart, pk=pk)
            cart_item.delete()
            return redirect(reverse_lazy('cart'), status=302)
        else:
            message = "To edit this exclusive event, you need to either log into your account or create an account with us"
            return render (request, 'account.html', {'message':message}, status=401)

