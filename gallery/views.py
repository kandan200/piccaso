from django.shortcuts import render
from app.models import EventImage, PublicEvent
from django.shortcuts import render, get_list_or_404

# Create your views here.
def gallery(request):
    items = EventImage.objects.all()
    return render(request, 'gallery.html', {'items':items}, status=200)

def gallery_item(request, pk):
    item = EventImage.objects.get(pk=pk)
    return render(request, 'gallery_item.html', {'item':item}, status=200)

def past_events_view(request):
    events = PublicEvent.objects.all()
    return render(request, 'past_events.html', {'events':events}, status=200)

def event_gallery_view(request, pk):
    event = PublicEvent.objects.get(pk=pk)
    event_gallery = get_list_or_404(EventImage, event=event)
    return render(request, 'event_gallery.html', {'images':event_gallery, 'event':event}, status=200)
