from django.db import models
import cloudinary
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    profile_photo=cloudinary.models.CloudinaryField('image',null=True,blank=True)
    bio=models.CharField(max_length=100)
    editor=models.ForeignKey(User,on_delete=models.CASCADE)
    
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

    def __str__(self):
        return self.destname

    @classmethod
    def get_all_destinations(cls):
        alldest=cls.objects.all()
        return alldest


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












