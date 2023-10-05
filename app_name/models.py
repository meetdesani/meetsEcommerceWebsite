from django.db import models
from django.utils import timezone

# Create your models here.
class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    remark = models.TextField()

    def __str__(self):
        return self.email
    

class User(models.Model):
    fname = models.CharField(max_length=200)
    lname = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    gender = models.CharField(max_length=200)
    mobile = models.IntegerField()
    password = models.CharField(max_length=200)
    cpassword = models.CharField(max_length=200)
    address = models.TextField()
    image = models.ImageField(upload_to="images/", blank = True, null = True)
    status = models.CharField(max_length=200, default = "deactivate")

    def _str__(self):
        return self.email
 

class Product(models.Model):
    BRANDS= (
        ('Apple','Apple'),
        ('Samsung','Samsung'),
        ('Dell', 'Dell'),
        ('Lenovo','Lenovo'),
        ('Google','Google'),
        ('Fitbit',"Fitbit"),
    )
    seller= models.ForeignKey(User, on_delete=models.CASCADE)
    product_brand= models.CharField(max_length=100, choices= BRANDS)
    product_model= models.CharField(max_length=100)
    product_price= models.IntegerField()
    product_desc= models.TextField()
    product_image= models.ImageField(upload_to='product_image')

    def __str__(self):
        return self.product_brand+ ' ' + self.product_model
    

class WishList(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    product= models.ForeignKey(Product, on_delete=models.CASCADE)
    date= models.DateField(default= timezone.now)
    
    def __str__(self):
        return self.user.fname+ ' ' + self.product.product_model



class Cart(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    product= models.ForeignKey(Product, on_delete=models.CASCADE)
    date= models.DateField(default= timezone.now)
    qty= models.IntegerField(default=1)
    price= models.IntegerField()
    total_price= models.IntegerField()

    def __str__(self):
        return self.user.fname+ ' ' + self.product.product_model
    

class ComplaintForm(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank= True, null=True)
    name= models.CharField(max_length=100, blank= True, null=True)
    seller= models.CharField(max_length=100)
    product= models.CharField(max_length=100)
    email= models.CharField(max_length=100)
    complaint= models.TextField() 


class Helpdesk(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank= True, null=True)
    name= models.CharField(max_length=100)
    seller= models.CharField(max_length=100)
    product= models.CharField(max_length=100)
    email= models.CharField(max_length=100)
    note= models.TextField()


class Checkout(models.Model):
    created_at= models.DateTimeField(auto_now_add=True, blank= True, null=True)
    name= models.CharField(max_length=100)
    email= models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)
    city= models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip= models.CharField(max_length=100)
    address= models.TextField()