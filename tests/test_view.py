from django.test import TestCase, Client, RequestFactory
from app.models import *
from datetime import date
from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect
from app.views import book_private_event, OrderView


class ViewTestCase(TestCase):
    #create seperate tests for logged-in and not-logged-in users
    @classmethod
    def setUpTestData(cls):
        artist = Artist.objects.create(first_name='kriss', last_name='killz')
        artist2 = Artist.objects.create(first_name='yng', last_name='kln')
        PublicEvent.objects.create(title='piiccasoBBQ', date=date.today(), venue='ciilantro', price=8000.00, collaborators=artist2, tags='#paint, #sip')
        public_event = PublicEvent.objects.create(title='piccasoBBQ', date=date.today(), venue='cilantro', price=8000, collaborators=artist, tags='#paint, #sip')
        PrivateEvent.objects.create(title='Debor at 30', date=date.today(), venue='debors bando', number_of_persons=15, contact='08162567299', email='debor@gmail.com')
        EventImage.objects.create(title='vibing', event=public_event, caption='its all about the moments we cant remember with the people we cant forget', tags='#friends4life')
        user = User.objects.create(username='admin', email='admin@gmail.com', password='password123')
        User.objects.create(username='yng', email='yng@gmail.com', password='password123')
        Artwork.objects.create(title='half of a rising sun', artist=artist, description='my minds expression of the biafran struggle', date=date.today(), price=30000, tags='#art #creativity', availability=True)
        PublicEventCart.objects.create(user=user, event=public_event, number_of_tickets=10, unit_price=public_event.price, price=80000)

    def test_home_view(self):
        response = self.client.get("/home/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text='<p>The art community</p>', html=True)
        self.assertTemplateUsed(response, 'home.html')
        
    def test_about_us_view(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')

    def test_contact_us_view(self):
        response = self.client.get('/contact-us/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact_us.html')

    def test_sign_in_view(self):
        response =  self.client.get('/sign-in/')
        response2 =  self.client.post('/sign-in/', data={'username':'admin', 'password': 'password123'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response2.status_code, 302)        
        self.assertTemplateUsed(response, 'sign_in.html')
        self.assertTemplateUsed(response2, 'home.html')

        
    def test_sign_up_view(self):
        response =  self.client.get('/sign-up/')
        response2 =  self.client.post('/sign-up/', data={'first_name':'uche', 'last_name':'kanu', 'username':'uche', 'email':'uche@gmail.com', 'contact': '08051452710', 'password':'password123', 'confirm_password':'password123'})
        client = get_object_or_404(Client, pk=1)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response2, expected_url='/home/', status_code=302, target_status_code=200)        
        self.assertEqual(response2.status_code, 302)
        self.assertEqual(str(client.first_name), 'uche')
        self.assertTemplateUsed(response, 'sign_up.html')
        self.assertTemplateUsed(response2, 'home.html')
        
        
    def test_book_public_event_view_loggedIn(self):
        user1 = User.objects.get(username='yng')
        event = PublicEvent.objects.get(title='piiccasoBBQ')
        self.client.force_login(user1)
        response1 =  self.client.get('/book-public-event/')
        response2 =  self.client.post('/book-public-event/', data={'user':user1, 'event':event, 'number_of_tickets':10, 'unit_price':500.00, 'price':800.00}, follow=True)    
        self.assertRedirects(response2, '/home/')
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 302)
        self.assertTemplateUsed(response1, 'book_public_event.html')
        self.assertTemplateUsed(response2, 'home.html')
        self.assertRedirects(response2, expected_url='/home/', status_code=302, target_status_code=200)
        cart_item = PublicEventCart.objects.get(user=user1)
        self.assertEqual(str(cart_item.event.venue), 'ciilantro')

    def test_book_public_event_view_not_loggedIn(self):
        user = User.objects.create(username='maazi', email='maazi@gmail.com', password='password123')
        event = PublicEvent.objects.get(title='piccasoBBQ')
        response1 =  self.client.get('/book-public-event/')
        response2 =  self.client.post('/book-public-event/', {'user':user, 'event':event, 'number_of_tickets':10, 'unit_price':event.price, 'price':80000}, follow=True)    
        # cart_item = PublicEventCart.objects.get(event=event)
        self.assertEqual(response1.status_code, 401)
        self.assertEqual(response2.status_code, 401)
        # self.assertTemplateUsed(response1, 'template/book_public_event.html')
        # self.assertTemplateUsed(response2, 'template/home.html')
        # self.assertEqual(str(cart_item.event.venue), 'cilantro')

    def test_book_private_event_view(self):
        response =  self.client.get('/book-private-event/')
        response2 =  self.client.post('/book-private-event/', {'title':'Debor at 30', 'date':date.today(), 'venue':'debors bando', 'number_of_persons':15, 'contact':'08162567299', 'email':'debor@gmail.com'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response2.status_code, 302)
        self.assertRedirects(response2, expected_url='/home/', status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'book_private_event.html')
        self.assertTemplateUsed(response2, 'home.html')

    def test_gallery_view(self):
        response =  self.client.get('/gallery/')
        self.assertTemplateUsed(response, 'gallery.html')
        self.assertEqual(response.status_code, 200)

    def test_gallery_item_view(self):
        event_image = EventImage.objects.get(title='vibing')
        response =  self.client.get(f'/gallery-item/{event_image.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gallery_item.html')

    def test_add_artwork_to_cart_view(self):
        artist = Artist.objects.create(first_name='kriss', last_name='killz')
        Artwork.objects.create(title='half of a rising sun', artist=artist, description='my minds expression of the biafran struggle', date=date.today(), price=30000, tags='#art #creativity', availability=True)
        response =  self.client.get('/artwork-to-cart/1/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url='/artworks-list/', status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'artworks.html')

    def test_past_events_view(self):
        response =  self.client.get('/past-events/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'past_events.html')

    def test_event_gallery_view(self):
        event = PublicEvent.objects.get(venue='cilantro')
        response = self.client.get(f'/event-gallery/{event.pk}/')    
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'event_gallery.html')
               
    def test_artwork_list_view(self):
        response = self.client.get('/artworks-list/')    
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'artworks.html')
        
    def test_artwork_view(self):
        artwork = Artwork.objects.get(title='half of a rising sun')
        response = self.client.get(f'/artwork/{artwork.pk}/')    
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'artwork.html')
        
    def test_cart_view(self):
        response = self.client.get('/cart/')    
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart.html')

    def test_edit_private_event_order_item_view(self):
        response =  self.client.get('/edit-private-event-order-item/1/')
        response2 =  self.client.put('/edit-private-event-order-item/1/', {'title':'Debor at 30', 'date':date.today(), 'venue':'Moved to lagos', 'number_of_persons':15, 'contact':'08162567299', 'email':'debor@gmail.com'})
        response3 =  self.client.delete('/edit-public-event-order-item/1/')
        event = PrivateEvent.objects.get(title='Debor at 30')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response2.status_code, 302)
        self.assertEqual(response3.status_code, 302)
        self.assertRedirects(response2, expected_url='/cart/', status_code=302, target_status_code=200)
        self.assertRedirects(response3, expected_url='/cart/', status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'edit_private_event.html')
        self.assertTemplateUsed(response2, 'cart.html')
        self.assertTemplateUsed(response3, 'cart.html')
        self.assertEqual(event.venue, 'Moved to lagos')

    def test_edit_public_event_order_item_view(self):
        user = User.objects.get(username='admin')
        event = PublicEvent.objects.get(title='piccasoBBQ')
        cart_item = PublicEventCart.objects.get(event=event)
        response =  self.client.get(f'/edit-public-event-order-item/{cart_item.pk}/')
        response2 =  self.client.patch(f'/edit-public-event-order-item/{cart_item.pk}/', {'number_of_tickets':30}, follow=True, content_type='multipart/form-data')
        response3 =  self.client.delete(f'/edit-public-event-order-item/{cart_item.pk}/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response2.status_code, 302)
        self.assertEqual(response3.status_code, 302)
        self.assertRedirects(response2, expected_url='/cart/', status_code=302, target_status_code=200)
        self.assertRedirects(response3, expected_url='/cart/', status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'edit_public_event.html')
        self.assertTemplateUsed(response2, 'cart.html')
        self.assertTemplateUsed(response3, 'cart.html')
        self.assertEqual(cart_item.number_of_tickets, 30)
    
    def test_edit_artwork_order_item_view(self):
        artist = Artist.objects.create(first_name='kriss', last_name='killz')
        artwork = Artwork.objects.create(title='half of a rising sun', artist=artist, description='my minds expression of the biafran struggle', date=date.today(), price=30000, tags='#art #creativity', availability=True)
        response =  self.client.delete('/edit-artwork-order-item/1/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url='/cart/', status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'cart.html')

    def test_order_view(self):
        response = self.client.post('/orders/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order.html')
        
    def test_log_out_view(self):
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        
        
class TestViewRequestFactory(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username='admin', email='admin@gmail.com', password='password123')
        
    def test_book_private_event(self):
        request = self.factory.get('/book-private-event/')
        request.user = self.user
        request2 =  self.factory.post('/book-private-event/', {'title':'Debor at 30', 'date':date.today(), 'venue':'debors bando', 'number_of_persons':15, 'contact':'08162567299', 'email':'debor@gmail.com'})
        request2.user = self.user
        response =  book_private_event(request)
        response2 =  book_private_event(request2)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response2.status_code, 302)
        self.assertRedirects(response2, expected_url='/home/', status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'book_private_event.html')
        self.assertTemplateUsed(response2, 'home.html')

    def test_book_private_event2(self):
        request = self.factory.get('/book-private-event/')
        # request.user = self.user
        request2 =  self.factory.post('/book-private-event/', {'title':'Debor at 30', 'date':date.today(), 'venue':'debors bando', 'number_of_persons':15, 'contact':'08162567299', 'email':'debor@gmail.com'})
        # request2.user = self.user
        response =  book_private_event(request)
        response2 =  book_private_event(request2)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response2.status_code, 401)
        self.assertRedirects(response2, expected_url='/home/', status_code=301, target_status_code=200)
        self.assertTemplateUsed(response, 'book_private_event.html')
        self.assertTemplateUsed(response2, 'home.html')

    def test_order_view(self):
        request = self.factory
        self.client.force_login(self.user)
        request.user = self.user
        view = OrderView()
        view.setup(request)
        
        response = view.create(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order.html')
        
