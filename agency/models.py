from django.db import models
import cloudinary
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from tinymce.models import HTMLField
import string
import random
# Create your models here.

class Profile(models.Model):
    profile_photo=cloudinary.models.CloudinaryField('image',null=True,blank=True)
    bio=models.CharField(max_length=100)
    editor=models.ForeignKey(User,on_delete=models.CASCADE)
    user_mac=models.CharField(max_length=1000,default="empty")
    
    def __str__(self):
        return self.editor.username

    def save_profile(self):
        self.save()
        
    @classmethod
    def single_profile(cls,user_id):
        '''
        function gets a single profile posted by id
        '''
        profile=cls.objects.get(editor=user_id)
        return profile

class Country(models.Model):
    countryname=models.CharField(max_length=30)
    country_image=cloudinary.models.CloudinaryField('image',null=True,blank=True)
    def __str__(self):
        return self.countryname

    @classmethod
    def get_all_countries(cls):
        allcount=cls.objects.all()
        return allcount


class Destination(models.Model):
    destincountry=models.ForeignKey(Country,on_delete=models.CASCADE)
    destname=models.CharField(max_length=30)
    address=models.CharField(max_length=30)
    pub_date = models.DateTimeField(auto_now_add=True)
    destination_image =cloudinary.models.CloudinaryField('image',null=True,blank=True)
    description=HTMLField(blank=True,null=True)
    price=models.DecimalField(max_digits=6,decimal_places=2,null=True)

    def __str__(self):
        return self.destname

    @classmethod
    def get_all_destinations(cls):
        alldest=cls.objects.all()
        return alldest

    @classmethod
    def search_by_destination(cls,search_term):
        dest_res=cls.objects.filter(destname__icontains=search_term)
        return dest_res

    @classmethod
    def search_by_country(cls,search_term):
        country_res=cls.objects.filter(destincountry__countryname__icontains=search_term)
        return country_res


class Package(models.Model):
    packagename=models.CharField(max_length=30)
    dest=models.ForeignKey(Destination,on_delete=models.CASCADE)
    price=models.DecimalField(max_digits=6,decimal_places=2)
    description=models.CharField(max_length=100)
    duration=models.IntegerField(default=1)

class Order(models.Model):
    customer=models.ForeignKey(Profile,on_delete=models.CASCADE)
    destination=models.ForeignKey(Destination,on_delete=models.CASCADE)
    package=models.ForeignKey(Package,on_delete=models.CASCADE)

class Reviews(models.Model):
    review_image=cloudinary.models.CloudinaryField('image',null=True,blank=True)
    reviewer=models.ForeignKey(User,on_delete=models.CASCADE)
    review=models.CharField(max_length=100)
    review_date=models.DateTimeField(auto_now_add=True)

class Wishlist(models.Model):
    destination=models.ForeignKey(Destination,on_delete=models.CASCADE)
    user_mac=models.CharField(max_length=1000)

    def __str__(self):
        return self.destination

class Subscribe(models.Model):
    name=models.ForeignKey(User,on_delete=models.CASCADE)
    email=models.CharField(max_length=1000,null=True)
    def __str__(self):
        return self.name.username

class Cart(models.Model):
    user_mac=models.CharField(max_length=1000)
    dest=models.ManyToManyField(Destination)
    total=models.IntegerField(default=0)
    updated=models.DateTimeField(auto_now=True)
    timestamp=models.DateField(auto_now_add=True)
    ordered=models.BooleanField(default=False)
    receipt_no=models.CharField(null=True,blank=True,max_length=1000)
    payment_method=models.CharField(default="Other",max_length=100)
    phone_no=models.CharField(null=True,blank=True,max_length=100)
    finished=models.BooleanField(default=False)

    def __str__(self):
        return self.user_mac

    def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars)for _ in range(size))
    

class BookedDest(models.Model):
    destination=models.ForeignKey(Destination,on_delete=models.CASCADE)
    user_mac=models.CharField(max_length=1000)
    paid=models.BooleanField(default=False)
    date=models.DateTimeField(auto_now_add=True)
    finished=models.BooleanField(default=False)

    def __str__(self):
        return self.destination.destname












