from django import forms
from . models import PublicEventCart, PrivateEvent, Client, Artwork

class SignUpForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        
class SignInForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['username', 'password']

class PublicEventBookingForm(forms.ModelForm):
    class Meta:
        model = PublicEventCart
        fields = '__all__'
               
class PrivateEventBookingForm(forms.ModelForm):
    class Meta:
        model = PrivateEvent
        fields = '__all__'
        
class EditPublicEventOrderItemForm(forms.ModelForm):
    class Meta:
        model = PublicEventCart
        fields = '__all__'
        