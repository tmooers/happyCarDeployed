from django.db import models
from django.utils import timezone
from django.urls import reverse


# Create your models here.

# Customer model

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=50)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now_add=True)

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        self.updated_date = timezone.now()
        self.save()

    def __str__(self):
        return '%s, %s' % (self.first_name, self.last_name)


# PartType model (aka Category)

class PartType(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:part_list_by_category', args=[self.slug])


# Part model

class Part(models.Model):
    part_type = models.ForeignKey(PartType, related_name='parts', on_delete=models.CASCADE)
    part_name = models.CharField(max_length=200, db_index=True)
    part_number = models.CharField(max_length=50, db_index=True)
    part_description = models.TextField(blank=True)
    part_image = models.ImageField(upload_to='part_uploads/% Y/% m/% d/', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now_add=True)

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        self.updated_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.part_name)

    class Meta:
        ordering = ('part_name',)


# define the Cart model
class Cart(models.Model):
    customer = models.ForeignKey(Customer, related_name='customer', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.customer)


# define the CartItem model used to store information about items in a cart
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='cart', on_delete=models.CASCADE)
    part = models.ForeignKey(Part, related_name='part', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.part)

    class Meta:
        ordering = ('cart',)


# define the Order model
class Order(models.Model):
    order_number = models.AutoField(primary_key=True, )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    email = models.EmailField(max_length=250)
    shipping_address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=10)
    status = models.CharField(max_length=25,
                              choices=[('R', 'Received'), ('P', 'Processing'), ('S', 'Shipped'), ('D', 'Delivered'),
                                       ('B', 'Back Order')], default='Received')
    comments = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now_add=True)

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        self.updated_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.order_number)


# define the order items

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order', on_delete=models.CASCADE)
    part = models.ForeignKey(Part, related_name='order_part', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_date = models.DateTimeField(default=timezone.now)

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.order)
