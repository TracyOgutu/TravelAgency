from django.shortcuts import render,redirect
from .models import Destination,Country,Profile
from django.db.models import Count
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import NewProfileForm
from django.contrib import messages

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

@login_required(login_url='/accounts/login/')
def logout_function(request):
    logout(request)
    return redirect('welcome')

@login_required(login_url='/accounts/login/')
def new_profile(request):
    '''
    Used for creating a new profile for the user. It includes a profile photo and a bio
    '''
    current_user = request.user
    if request.method == 'POST':
        form = NewProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.editor = current_user
            profile.save()
        return redirect('welcome')

    else:
        form = NewProfileForm()
    return render(request, 'new_profile.html', {"form": form})

@login_required(login_url='/accounts/login/')
def display_profile(request,user_id):
    '''
    View for displaying the profile for a single user
    '''
    try:
        single_profile=Profile.single_profile(user_id)              
        return render(request,'profiledisplay.html',{"profile":single_profile})
    except Profile.DoesNotExist:
        messages.info(request,'The user has not set a profile yet')
        return redirect('welcome')




