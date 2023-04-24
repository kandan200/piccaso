from decimal import Decimal
from rest_framework import serializers
from .models import PublicEvent, PublicEventCart, PublicEventOrderItem, PrivateEvent, PrivateEventCart, PrivateEventOrderItem, Order, Artist, Artwork, ArtworkCart, ArtworkOrderItem, Client
import bleach
from django.contrib.auth.models import User, Group
from django.forms import ValidationError, model_to_dict
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = '__all__'

class PublicEventSerializer(serializers.ModelSerializer):
    collaborators = ArtistSerializer(write_only=True)
    
    class Meta:
        model = PublicEvent
        fields = '__all__'
        
class PrivateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateEvent
        fields = '__all__'
        
class ArtworkSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer()
    
    class Meta:
        model = Artwork
        fields = '__all__'
        
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['username']

class OrderSerializer(serializers.ModelSerializer):
    user = ClientSerializer()

    class Meta:
        model = Order
        fields = '__all__'
        
class ArtworkOrderItemSerializer(serializers.ModelSerializer):
    order = OrderSerializer()
    item = ArtworkSerializer()
    
    class Meta:
        model = ArtworkOrderItem
        fields = '__all__'

class PublicEventOrderItemSerializer(serializers.ModelSerializer):
    order = OrderSerializer()
    event = PublicEventSerializer()

    class Meta:
        model = PublicEventOrderItem
        fields = '__all__'

class PrivateEventOrderItemSerializer(serializers.ModelSerializer):
    order = OrderSerializer()
    event = PrivateEventSerializer()

    class Meta:
        model = PrivateEventOrderItem
        fields = '__all__'