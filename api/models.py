import uuid
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    auto_id = models.PositiveIntegerField(db_index=True, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='%(class)s_created', null=True)
    updater = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='%(class)s_updated', null=True)
    
    def save(self, *args, **kwargs):
        if not self.auto_id:
            # Generate a new auto_id for new instances
            last_instance = self.__class__.objects.order_by('-auto_id').first()
            if last_instance:
                self.auto_id = last_instance.auto_id + 1
            else:
                self.auto_id = 1
        super().save(*args, **kwargs)


    class Meta:
        abstract = True


class Restaurant(BaseModel):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()

    class Meta:
        db_table = 'restaurant'
        verbose_name = _('Restaurant')
        verbose_name_plural = _('Restaurants')
        ordering = ('-date_added',)
        
    def __str__(self):
        return self.name


class MenuItem(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    cuisine = models.CharField(max_length=100)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(upload_to='menu_item_photos')

    class Meta:
        db_table = 'menu_item'
        verbose_name = _('Menu Item')
        verbose_name_plural = _('Menu Items')
        ordering = ('-date_added',)
        
    def __str__(self):
        return self.name
    

class User(AbstractUser):
    delivery_address = models.CharField(max_length=200)
    

class Order(BaseModel):
    STATUS_CHOICES = (
        ('pending', _('Pending')),
        ('confirmed', _('Confirmed')),
        ('preparation', _('In Preparation')),
        ('dispatched', _('Dispatched')),
        ('delivered', _('Delivered')),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    menu_items = models.ManyToManyField(MenuItem)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    class Meta:
        db_table = 'order'
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        ordering = ('-date_added',)
        
    def __str__(self):
        return f"{self.id}"
