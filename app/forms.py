from django import forms
from . models import PublicEventCart, PrivateEvent, Customer, Artwork

class SignUpForm(forms.Form):
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    email = forms.EmailField()
    contact = forms.CharField(max_length=200)
    password = forms.CharField(max_length=200)
    confirm_password = forms.CharField(max_length=200)
    is_active = forms.BooleanField()
    is_staff = forms.BooleanField()

class SignInForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(max_length=200)

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
        fields = ['number_of_tickets']

class PasswordResetRequestForm(forms.Form):
    email= forms.EmailField()
    
class PasswordResetConfirmForm(forms.Form):
    uid = forms.CharField(max_length=250)
    token = forms.CharField(max_length=250)
    password = forms.CharField(max_length=250)
    re_password = forms.CharField(max_length=250)
    
class AccountActivationForm(forms.Form):
    uid = forms.CharField(max_length=200)
    token = forms.CharField(max_length=250)