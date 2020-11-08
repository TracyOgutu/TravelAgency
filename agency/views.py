from django.shortcuts import render,redirect
from .models import Destination,Country,Profile,Reviews,Wishlist,Subscribe
from django.db.models import Count
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist,ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import NewProfileForm,NewReviewForm
from django.contrib import messages
from getmac import get_mac_address as gma
from django.contrib.auth.models import User
import requests
from django.core.mail.message import BadHeaderError
from django.core.validators import validate_email
from django.http import HttpResponse
from django.core.mail import send_mail

# Create your views here.
def welcome(request):
    try:
        countries=Country.objects.annotate(number_of_destinations=Count('destination'))
        print('........................number of destinations in the country........................')
        print(countries)
        allreviews=Reviews.objects.all()
    except ObjectDoesNotExist:
        raise Http404()

    return render(request, 'welcome2.html',{"countries":countries,"reviews":allreviews})

def about(request):

    return render(request,'about.html')

def contact(request):

    return render(request,'contact.html')

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

@login_required(login_url='/accounts/login/')
def make_review(request):
    current_user = request.user
    current_id=request.user.id
    print('...................I am the current user....................')
    print(current_id)
    if request.method == 'POST':
        form = NewReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = current_user
            review.save()
        return redirect('welcome')

    else:
        form = NewReviewForm()
    return render(request, 'make_review.html', {"form": form})
@login_required(login_url='/accounts/login/')
def displaywishlist(request):
    try:
        wishlist_items=Wishlist.objects.filter(user_mac=gma())
    except Wishlist.DoesNotExist:
        wishlist_items=[]
    
    return render(request,'wishlist.html',{"wishitems":wishlist_items})

@login_required(login_url='/accounts/login/')
def addtowishlist(request,id):
    dest=Destination.objects.get(id=id)
    try:
        wishlist_exists=Wishlist.objects.get(user_mac=gma(),destination=dest)
        messages.info(request,"This destination is already in your wishlist")
        return redirect("displaywishlist")
    
    except Wishlist.DoesNotExist:
        new_wishlist=Wishlist(destination=dest,user_mac=gma())
        new_wishlist.save()
        messages.info(request,"The destination has been added to your wishlist")
        return redirect('displaywishlist')
@login_required(login_url='/accounts/login/')
def deletefromwishlist(request,id):
    try:
        dest_del=Wishlist.objects.get(user_mac=gma(),destination=id)
        dest_del.delete()
        messages.info(request,"The destination has been successfully deleted from your wishlist")

        return redirect('displaywishlist')
    except ObjectDoesNotExist:
        raise Http404()

# @login_required(login_url='/accounts/login/')
# def subscribe(request):
#     if request.user.is_authenticated:
#         if request.method=="POST":
#             useremail=request.POST.get("email")
#             print('........................USER---EMAIL........................')
#             print(useremail)
#             try:
#                 validate_email( useremail )
#                 name=request.user
#                 print('........................NAME --- SUBSCRIBER........................')
#                 print(name)
#                 subscribe_email(name,useremail)
#                 new_subscriber=Subscribe(name=request.user,email=useremail)
#                 new_subscriber.save()
#                 messages.info(request, 'Successfully subscribed to Travel Agency! Please check your email')
#                 return redirect('welcome')
#             except ValidationError:
#                 return False
#             # except:
#             #     messages.info(request,'Please enter a valid email address.')
#             #     return redirect('welcome')
#         else:
#             messages.info(request,'Please try again. Something went wrong.')
#             return redirect('welcome')
#     else:
#         return redirect('welcome')

@login_required(login_url='/accounts/login/')
def send_email(request):
    subject = request.POST.get('subject', '')
    message = request.POST.get('message', '')
    from_email = request.POST.get('email', '')
    if subject and message and from_email:
        try:
            send_mail(subject, message, from_email, ['beastmater064@gmail.com'])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return redirect('welcome')
    else:
        # In reality we'd use a form class
        # to get proper validation errors.
        return HttpResponse('Make sure all fields are entered and valid.')




    




