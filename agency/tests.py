from django.test import TestCase

# Create your tests here.
from .models import Customer,Destination,Package,Order

class CustomerTestClass(TestCase):
    # Set up method
    def setUp(self):
        self.rita=Customer(name='rita',email='rita@gmail.com')

    #testing instance
    def test_instance(self):
        self.assertTrue(isinstance(self.rita,Customer))
    
    #testing the save method
    def test_save_method(self):
        self.rita.save_customer()
        customers=Customer.objects.all()
        self.assertTrue(len(customers)>0)

    

    
