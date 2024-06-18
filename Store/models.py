from django.db import models
from django.urls import reverse
# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=250,unique=True)
    slug=models.SlugField(max_length=250,unique=True)
    description=models.TextField(blank=True)
    image=models.ImageField(upload_to='category',blank=True)

    class Meta:
        ordering=('name',)
        verbose_name='category'
        verbose_name_plural='categories'

    def get_url(self):
        return reverse('product_by_category',args=[self.slug])

    def __str__(self):
        return self.name

class Prod(models.Model):
    name=models.CharField(max_length=250,unique=True)
    slug=models.SlugField(max_length=250,unique=True)
    description=models.TextField(blank=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    image=models.ImageField(upload_to='product',blank=True)
    stock=models.IntegerField()
    available=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)


    class Meta:
        ordering=('name',)
        verbose_name='product'
        verbose_name_plural='products'

    def get_url(self):
        return reverse('product_details',args=[self.category.slug,self.slug])

    def __str__(self):
        return self.name

class Cart(models.Model):
    cart_id=models.CharField(max_length=250,blank=True)
    date_added=models.DateField(auto_now_add=True)

    class Meta:
        db_table='Cart'
        ordering=['date_added']

    def __str__(self):
        return self.cart_id

class Cartitem(models.Model):
    product=models.ForeignKey(Prod,on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    active=models.BooleanField(default=True)

    class Meta:
        db_table='Cartitem'

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product

class Order(models.Model):
    csrfmiddlewaretoken=models.CharField(max_length=250,blank=True)
    token=models.CharField(max_length=250,blank=True)
    total=models.DecimalField(max_digits=10,decimal_places=2,verbose_name='INR Order Total')
    emailAddress=models.EmailField(max_length=250,blank=True,verbose_name='Email Address')
    token_type=models.CharField(max_length=250,blank=True)
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table='Order'
        ordering=['-created']

    def __str__(self):
        return str(self.id)

class OrderItem(models.Model):
    product=models.CharField(max_length=250)
    quantity=models.IntegerField()
    price=models.DecimalField(max_digits=10,decimal_places=2,verbose_name='INR Price')
    order=models.ForeignKey(Order,on_delete=models.CASCADE)

    class Meta:
        db_table='OrderItem'

    def sub_total(self):
        return self.quantity * self.price

    def __str__(self):
        return self.product
