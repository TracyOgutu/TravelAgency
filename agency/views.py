from django.shortcuts import render
from .models import Destination,Country
from django.db.models import Count
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def welcome(request):
   
    countries=Country.objects.annotate(number_of_destinations=Count('destination'))
    print('........................number of destinations in the country........................')
    print(countries)
    return render(request, 'welcome2.html',{"countries":countries})

def single_country(request,country_id):
    try:
        country = Country.objects.get(id =country_id)
        dest=Destination.objects.filter(destincountry=country_id)
        
    except ObjectDoesNotExist:
        raise Http404()
    return render(request,"country.html", {"single_country":country,"dest_items":dest})

def single_destination(request, destiinationid):
    try:
        destination=Destination.objects.get(id=destiinationid)
    except ObjectDoesNotExist:
        raise Http404()
    return render(request,"singledestination.html",{"destination":destination})

def all_destinations(request):
    try:
        all_dest=Destination.objects.all()
    except ObjectDoesNotExist:
        raise Http404()
    return render(request,"alldest.html",{"all_dest":all_dest})

