from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
class ClientAccountManager(BaseUserManager):
    def create_user(self, first_name, email, contact, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(first_name=first_name, email=email, contact=contact)
        user.set_password(password)
        user.save()
        return user

# class Customer(AbstractBaseUser, PermissionsMixin):
class Customer(models.Model):
    first_name = models.CharField(max_length=200, verbose_name='First name')
    last_name = models.CharField(max_length=200, verbose_name='Last Name')
    email = models.EmailField(verbose_name="Email", unique=True)
    contact = models.CharField(max_length=200, verbose_name='Phone Number')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
#     objects = ClientAccountManager()
    
#     USERNAME_FIELD ='email'
#     REQUIRED_FIELDS = ['first_name', 'contact']
    
#     def get_full_name(self):
#         return self.first_name + "" + self.last_name
    
#     def get_short_name(self):
#         return self.first_name
    
#     def __str__(self):
#         return self.email
    
    
class Artist(models.Model):
    first_name = models.CharField(max_length=200, verbose_name='First Name')
    last_name = models.CharField(max_length=200, verbose_name='Last Name')
    # avatar = models.ImageField()
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
    
class PublicEvent(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    date = models.DateField()
    venue = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    collaborators = models.ForeignKey(Artist, on_delete=models.DO_NOTHING)
    tags = models.CharField(max_length=200)
    
    def __str__(self):
        return self.title


class PrivateEvent(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    date = models.DateField()
    venue = models.CharField(max_length=500)
    number_of_persons = models.IntegerField(verbose_name='Number of participants')
    contact = models.CharField(max_length=200, verbose_name='Contact number', blank=True)
    email = models.EmailField()
    
    def __str__(self):
        return self.title


class EventImage(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    event = models.ForeignKey(PublicEvent, on_delete=models.DO_NOTHING)
    caption = models.CharField(max_length=1000)
    tags = models.CharField(max_length=200)
    
    def __str__(self):
        return self.title

    
class Artwork(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)
    date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=3)
    tags = models.CharField(max_length=200)
    availability = models.BooleanField(default=False)
    # image = models.ImageField()
    
    def __str__(self):
        return self.title

    
class PublicEventCart(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    event = models.ForeignKey(PublicEvent, on_delete=models.CASCADE)
    number_of_tickets = models.IntegerField(verbose_name='Number of tickets')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        unique_together = ('event','user')
        
    def __str__(self):
        return self.user.first_name +' : '+ self.event.title
      
    
class ArtworkCart(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    item = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('item','user')
        
    def __str__(self):
        return self.user.first_name +' : '+ self.item.title
    
    
class PrivateEventCart(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    event = models.ForeignKey(PrivateEvent, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('event','user')
        
    def __str__(self):
        return self.user.first_name +' : '+ self.event.title

               
class Order(models.Model): 
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField(db_index=True)
    
    def __str__(self):
        return self.user.first_name +' : '+ str(self.date)


class PrivateEventOrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    event = models.ForeignKey(PrivateEvent, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('order','event')
        
    def __str__(self):
        return self.order.user.first_name +' : '+ self.event.title
    

class PublicEventOrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    event = models.ForeignKey(PublicEvent, on_delete=models.CASCADE)
    number_of_tickets = models.SmallIntegerField(verbose_name='Number of tickets')
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    
    class Meta:
        unique_together = ('order','event')
        
    def __str__(self):
        return self.order.user.first_name +' : '+ self.event.title
    
    
class ArtworkOrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        unique_together = ('order','item')
        
    def __str__(self):
        return self.order.user.first_name +' : '+ self.item.title
    
