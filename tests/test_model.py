from django.test import TestCase
from app.models import *
from datetime import date
from django.contrib.auth.models import User


class ModelsTestCase(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.artist = Artist.objects.create(first_name='kriss', last_name='killz')
        cls.public_event = PublicEvent.objects.create(title='piccasoBBQ', date=date.today(), venue='cilantro', price='8000', collaborators=cls.artist, tags='#paint, #sip')
        cls.private_event = PrivateEvent.objects.create(title='Debor at 30', date=date.today(), venue='debors bando', number_of_persons=15, contact='08162567299', email='debor@gmail.com')
        cls.event_image = EventImage.objects.create(title='vibing', event=cls.public_event, caption='its all about the moments we cant remember with the people we cant forget', tags='#friends4life')
        cls.user = User.objects.create(username='admin', email='admin@gmail.com', password='password123')
        cls.artwork = Artwork.objects.create(title='half of a rising sun', artist=cls.artist, description='my minds expression of the biafran struggle', date=date.today(), price=30000, tags='#art #creativity', availability=True)
        cls.public_event_cart_item = PublicEventCart.objects.create(user=cls.user, event=cls.public_event, number_of_tickets=10, unit_price=cls.public_event.price, price=80000)
        cls.artwork_cart =ArtworkCart.objects.create(user=cls.user, item=cls.artwork)
        cls.private_event_cart_item = PrivateEventCart.objects.create(user=cls.user, event=cls.private_event)
        cls.order= Order.objects.create(user=cls.user, total=1000, date=date.today())
        cls.private_event_order_item = PrivateEventOrderItem.objects.create(order=cls.order, event=cls.private_event)
        cls.public_event_order_item = PublicEventOrderItem.objects.create(order=cls.order, event=cls.public_event, number_of_tickets=cls.public_event_cart_item.number_of_tickets, price=cls.public_event_cart_item.price, unit_price=cls.public_event_cart_item.unit_price)
        cls.artwork_order_item = ArtworkOrderItem.objects.create(order=cls.order, item=cls.artwork, price=cls.artwork.price)
        
    def tearDown(self):
        artist = Artist.objects.get(first_name='kriss')
        public_event= PublicEvent.objects.get(title='piccasoBBQ')
        private_event =PrivateEvent.objects.get(title='Debor at 30')
        event_image = EventImage.objects.get(title='vibing')
        user = User.objects.get(username='admin')
        artwork = Artwork.objects.get(title='half of a rising sun')
        public_event_cart_item = PublicEventCart.objects.get(event=public_event)
        artwork_cart_item = ArtworkCart.objects.get(item=artwork)
        private_event_cart_item = PrivateEventCart.objects.get(event=private_event)
        private_event_order_item = PrivateEventOrderItem.objects.get(event=private_event)
        public_event_order_item = PublicEventOrderItem.objects.get(event=public_event)
        artwork_order_item = ArtworkOrderItem.objects.get(item=artwork)
        order= Order.objects.get(user=user)

        artwork_order_item.delete()
        public_event_order_item.delete()
        private_event_order_item.delete()
        private_event_cart_item.delete()
        artwork_cart_item.delete()
        public_event_cart_item.delete()
        order.delete()
        artwork.delete()
        user.delete()
        event_image.delete()
        private_event.delete()
        public_event.delete()
        artist.delete()
        
    def test_artist(self):
        artist = Artist.objects.get(first_name='kriss')
        self.assertEqual(str(artist), 'kriss killz')
        
    def test_public_event(self):
        public_event= self.public_event
        self.assertEqual(str(public_event), 'piccasoBBQ')
        with self.assertRaisesMessage(ValueError, "invalid literal for int()"):
            int(public_event.price)
        
    def test_private_event(self):
        private_event= PrivateEvent.objects.get(title='Debor at 30')
        self.assertEqual(str(private_event), 'Debor at 30')
        
    def test_event_image(self):
        event_image = EventImage.objects.get(title='vibing')
        self.assertEqual(str(event_image), 'vibing')
        
    def test_artwork(self):
        artwork = Artwork.objects.get(title='half of a rising sun')
        self.assertEqual(str(artwork), 'half of a rising sun')
       
    def test_public_event_cart_item(self):
        public_event= PublicEvent.objects.get(title='piccasoBBQ')
        public_event_cart_item = PublicEventCart.objects.get(event=public_event)
        self.assertEqual(str(public_event_cart_item.event), 'piccasoBBQ')
        
    def test_private_event_cart_item(self):
        private_event= PrivateEvent.objects.get(title='Debor at 30')
        private_event_cart_item = PrivateEventCart.objects.get(event=private_event)
        self.assertEqual(str(private_event_cart_item.event), 'Debor at 30')
        
    def test_artwork_cart_item(self):
        artwork = Artwork.objects.get(title='half of a rising sun')
        artwork_cart_item = ArtworkCart.objects.get(item=artwork)
        self.assertEqual(str(artwork_cart_item.item), 'half of a rising sun')
        
    def test_private_event_order_item(self):
        private_event= PrivateEvent.objects.get(title='Debor at 30')
        private_event_order_item = PrivateEventOrderItem.objects.get(event=private_event)
        self.assertEqual(str(private_event_order_item.event), 'Debor at 30')
        self.assertEqual(str(private_event_order_item.order.user.username), 'admin')
        self.assertEqual(str(private_event_order_item), 'admin : Debor at 30')

    def test_public_event_order_item(self):
        public_event= PublicEvent.objects.get(title='piccasoBBQ')
        public_event_cart_item = PublicEventCart.objects.get(event=public_event)
        public_event_order_item = PublicEventOrderItem.objects.get(event=public_event)
        self.assertEqual(str(public_event_order_item.event), 'piccasoBBQ')
        self.assertEqual(str(public_event_order_item.order.user.username), 'admin')
        self.assertEqual(str(public_event_order_item), 'admin : piccasoBBQ')

       
    def test_artwork_order_item(self):
        artwork = Artwork.objects.get(title='half of a rising sun')       
        artwork_order_item = ArtworkOrderItem.objects.get(item=artwork)
        self.assertEqual(str(artwork_order_item.order.user), 'admin')
        self.assertEqual(str(artwork_order_item.price), str(artwork.price))
        self.assertEqual(str(artwork_order_item.item), 'half of a rising sun')
