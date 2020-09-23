from django.shortcuts import render
from .models import Destination

# Create your views here.
def welcome(request):

    destination = Destination.get_all_destinations()
    return render(request, 'welcome.html',{"destination":destination})
