from django.db import models
import datetime
import os
from django.contrib.auth.models import User

# Create your models here.

def get_file_path(request,filename):
   original_filename=filename
   nowTime=datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')  
   filename="%s%s" % (nowTime,original_filename)  
   return os.path.join('uploads/', filename ) 




class Category(models.Model):
    slug=models.CharField(max_length=150,null=False,blank=False)
    restaurant_name=models.CharField(max_length=150,null=False,blank=False)
    image=models.ImageField( upload_to=get_file_path, null=True,blank=True) 
    description =models.TextField(max_length=500, null=False,blank=False) 
    status=models.BooleanField(default=False,help_text="0=default, 1=Hidden")
    trending=models.BooleanField(default=False,help_text="0=default, 1=Trending")
    meta_title=models.CharField(max_length=150,null=False,blank=False)
    meta_keyword=models.CharField(max_length=150,null=False,blank=False)
    meta_description=models.TextField(max_length=500,null=False,blank=False)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.restaurant_name

class Product(models.Model):
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    slug=models.CharField(max_length=150,null=False,blank=False)
    food_name=models.CharField(max_length=150,null=False,blank=False)
    food_image=models.ImageField( upload_to=get_file_path, null=True,blank=True)
    description =models.CharField(max_length=250, null=False,blank=False)  
    price=models.FloatField(null=False,blank=False)
    status=models.BooleanField(default=False,help_text="0=default, 1=Hidden")
    trending=models.BooleanField(default=False,help_text="0=default, 1=Trending")
    tag=models.CharField(max_length=150,null=False,blank=False)
    meta_title=models.CharField(max_length=150,null=False,blank=False)
    meta_keyword=models.CharField(max_length=150,null=False,blank=False)
    meta_description=models.TextField(max_length=500,null=False,blank=False)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.food_name        


class CartItem(models.Model):
        product = models.ForeignKey(Product, on_delete=models.CASCADE)
        quantity = models.PositiveIntegerField(default=0)
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        date_added = models.DateTimeField(auto_now_add=True)
        total_price= models.DecimalField(max_digits=10, decimal_places=2,default=1)    
     