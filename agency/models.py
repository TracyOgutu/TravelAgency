from django.db import models

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=30)
    email=models.EmailField()

    def __str__(self):
        return self.name

    def save_customer(self):
        self.save()


class Destination(models.Model):
    name=models.CharField(max_length=30)
    address=models.CharField(max_length=30)
    pub_date = models.DateTimeField(auto_now_add=True)

    @classmethod
    def get_all_destinations(cls):
        alldest=cls.objects.all()
        return alldest

class Package(models.Model):
    name=models.CharField(max_length=30)
    dest=models.ForeignKey(Destination,on_delete=models.CASCADE)
    price=models.DecimalField(max_digits=6,decimal_places=2)
    description=models.CharField(max_length=100)
    duration=models.IntegerField(default=1)

class Order(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    destination=models.ForeignKey(Destination,on_delete=models.CASCADE)
    package=models.ForeignKey(Package,on_delete=models.CASCADE)






