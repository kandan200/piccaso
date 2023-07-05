from django.test import TestCase, Client
from app.forms import *
from datetime import date
from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect

class TestFormsTestCase(TestCase):
    
    def test_sign_up_form(self):
        form = SignUpForm(first_name='kanu', last_name='chibuzo', username='kandan', email='kanuchibuzo@yahoo.com', contact='08162567299', password='password123', confirm_password='password123')
        form2 = SignUpForm(first_name='kanu', last_name='chibuzo', username='kandan', email='kanuchibuzo@yahoo.com', contact= 8162567299, password='password123', confirm_password='password123')
        form = SignUpForm(first_name='kanu', last_name='chibuzo', username='kandan', email='kanuchibuzo@yahoo.com', contact='08162567299', password='password123', confirm_password='password123')
        self.assertFormError(form, field='contact', errors=[], msg_prefix='No error noted')
        self.assertFormError(form2, field='contact', errors=ValueError, msg_prefix='Field only accepts string characters and not numeric data')
        self.assertFormError(form, field=None, errors=[], msg_prefix='Duplicate data enteres. Form instance with above detaails already stored in database')

    def test_sign_in_form(self):
        form = SignInForm()
        pass
    
    def test_private_event_booking_form(self):
        form = PrivateEventBookingForm()
        pass
    
    def test_public_event_booking_form(self):
        form = PublicEventBookingForm()
        pass
    
    def test_edit_public_event_booking_form(self):
        form = EditPublicEventOrderItemForm()
        pass