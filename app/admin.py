from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Artist)
admin.site.register(Artwork)
admin.site.register(ArtworkCart)
admin.site.register(ArtworkOrderItem)
admin.site.register(PublicEvent)
admin.site.register(PrivateEvent)
admin.site.register(PrivateEventCart)
admin.site.register(PrivateEventOrderItem)
admin.site.register(PublicEventCart)
admin.site.register(PublicEventOrderItem)
admin.site.register(Customer)
admin.site.register(EventImage)
admin.site.register(Order)

