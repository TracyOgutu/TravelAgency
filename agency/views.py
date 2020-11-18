from django.shortcuts import render,redirect,get_object_or_404
from .models import Destination,Country,Profile,Reviews,Wishlist,Subscribe,Cart,BookedDest
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
from django.core.validators import validate_email
from django.http import HttpResponse
from django.core.mail import send_mail,BadHeaderError
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.conf import settings
import uuid 
import random
from paypal.standard.forms import PayPalPaymentsForm
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

@login_required(login_url='/accounts/login/')
@csrf_protect
def send_email(request):
    subject = request.POST.get('subject', '')
    message = request.POST.get('message', '')
    from_email = request.POST.get('email', '')
    if subject and message and from_email:
        try:
            send_mail(subject, message, from_email, ['travelagency477@gmail.com'])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return redirect('welcome')
    else:
        # In reality we'd use a form class
        # to get proper validation errors.
        return HttpResponse('Make sure all fields are entered and valid.')

@login_required(login_url='/accounts/login/')
@csrf_protect
def subscribe(request):
    subject = 'Welcome to Travel Agency.'
    message = 'Thank you for subscribing. Anticipate exciting updates on magical destinations! ' 
    user_email=request.POST.get('useremail', '')
    from_email = 'travelagency477@gmail.com'
    if user_email:
        try:
            send_mail(subject, message, from_email, [user_email])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        new_subscriber=Subscribe(name=request.user,email=user_email)
        new_subscriber.save()
        messages.info(request, 'Successfully subscribed to Travel Agency! Please check your email')
        return redirect('welcome')
    else:
        # In reality we'd use a form class
        # to get proper validation errors.
        return HttpResponse('Make sure all fields are entered and valid.')


def search_country(request):
    if 'countrysearch' in request.GET and request.GET["countrysearch"]:
        search_term=request.GET.get("countrysearch")
        try:
            searched_country=Destination.search_by_country(search_term)
            message = f"{search_term}"
            return render(request, 'searchcountry.html',{"message":message,"country_results":searched_country})
            
        except Destination.DoesNotExist:
            messages.info(request,'No product found')
            return redirect('welcome')

    else:
        messsage="You haven't searched for a specific country"
        return render(request,'searchcountry.html',{"message":message})

def search_destination(request):
    if 'destsearch' in request.GET and request.GET["destsearch"]:
        search_terms=request.GET.get("destsearch")
        searched_dest=Destination.search_by_destination(search_terms)
        message=f"{search_terms}"
        return render(request,'searchdest.html',{"message":message,"dest_results":searched_dest})
        
    else:
        message="You haven't searched for a destination"
        return render(request,'searchdest.html',{"message":message})

@login_required(login_url='/accounts/login/')
def displaycart(request):
    try:
        cart_items=Cart.objects.filter(user_mac=gma(),ordered=False)
    except Cart.DoesNotExist:
        cart_items=[]
    
    return render(request,'cartdisplay.html',{"cartitems":cart_items})

@login_required(login_url='/accounts/login/')
@csrf_protect
def make_booking(request):
    dest_id=request.POST.get("dest_id")
    user_dest=Destination.objects.get(id=dest_id)
    print('****************USER_DESTINATION******************')
    print(user_dest)
    try:
        usercart=Cart.objects.get(user_mac=gma(),ordered=False)
        if usercart.ordered==False:
            destcart=usercart.dest.all()
            all_items=[]
            for onedest in destcart:
                all_items.append(onedest.destname)
            
            if user_dest.destname in all_items:
                messages.info(request,'Destination already exist.')
                return redirect('welcome')
            else:                       
                new_booking=BookedDest(destination=user_dest,user_mac=gma())
                new_booking.save()
                sub_total=user_dest.price
                usercart.dest.add(user_dest.id)
                usercart.total+=sub_total
                usercart.save()
                messages.info(request,'The destination successfully added to cart.Continue exploring or click booking summary to proceed to payment')
                return redirect('welcome')

    except Cart.DoesNotExist:
        new_booking=BookedDest(destination=user_dest,user_mac=gma())
        new_booking.save()

        sub_total=user_dest.price
        new_cart=Cart(user_mac=gma(),total=sub_total)
        new_cart.save()
        new_cart.dest.add(user_dest)
        new_cart.save()
        messages.info(request,'The destination successfully added to your cart.Continue exploring or click booking summary to proceed to payment')
        return redirect('welcome')  

@login_required(login_url='/accounts/login/')
@csrf_protect
def delete_from_booking(request,id):
    destination=Destination.objects.get(id=id)
    item_tobe_deleted=BookedDest.objects.get(destination=id,user_mac=gma(),paid=False)
    cost=destination.price

    user_cart=Cart.objects.get(user_mac=gma(),ordered=False)
    alldests=user_cart.dest.all()
    if len(alldests)==1:
        newtotal=0
        user_cart.total=newtotal
        user_cart.dest.remove(destination.id)
        user_cart.delete()
        item_tobe_deleted.delete()
        messages.info(request,'You have cleared your cart')
        return redirect('welcome')
    else:
        newtotal=user_cart.total-cost
        user_cart.total=newtotal
        user_cart.dest.remove(destination.id)
        user_cart.save()
        item_tobe_deleted.delete()

        messages.info(request,'Item successfully deleted from your cart')
        return redirect('welcome')
@login_required(login_url='/accounts/login/')
@csrf_protect
def booking_summary(request):
    try:
        book_dest=BookedDest.objects.filter(user_mac=gma(),paid=False)
    except BookedDest.DoesNotExist:
        book_dest=[]

    try:
        cart_items=Cart.objects.filter(user_mac=gma(),ordered=False)
    except Cart.DoesNotExist:
        cart_items=[]
    
    if len(book_dest)<1:
        messages.info(request,'You have not added anything to your cart.')
        return redirect('welcome')
    else:
        return render(request,'bookingsummary.html',{"book_dest":book_dest,"cartitems":cart_items})

@login_required(login_url='/accounts/login/')
@csrf_exempt
def process_payment(request):
    #Converting Kenya shillings to US Dollars
    API_KEY= settings.FIXER_ACCESS_KEY 
    url="http://data.fixer.io/api/latest?access_key="+API_KEY+"&symbols=KES,USD"
    response=requests.request("GET",url)
    html=response.json()
    kes=html['rates']['KES']
    usd=html['rates']['USD']
    final_usd=kes/usd

    #Checking out
    try:
        book_dest=BookedDest.objects.filter(user_mac=gma(),paid=False)
    except BookedDest.DoesNotExist:
        book_dest=[]

    try:
        user_cart=Cart.objects.get(user_mac=gma(),ordered=False)
        print('******************USER CART OBJECT***************')
        
        print(user_cart)
        # setting mac address to profile
        current_user=Profile.objects.get(editor=request.user)    
        user_cart.user_mac=current_user.user_mac
        current_user.save()
    except Cart.DoesNotExist:
        user_cart=[]

    
    total_in_usd=user_cart.total/final_usd
    list_of_dests=[]
    for dest in book_dest:
        list_of_dests.append(dest.destination.destname)

    host=request.get_host()
    paypal_dict={
        'business':settings.PAYPAL_RECEIVER_EMAIL,
        'amount':'%.2f' % total_in_usd,
        'item_name':'{}'.format(list_of_dests),
        'invoice': str(random.randint(00000,99999)),
        'currency_code':'USD',
        'notify_url':'http://{}{}'.format(host,'-gdgdj-travel-kahndbfh-gshdnhdjf-ksndshdj'),
        'return_url':'http://{}{}'.format(host,'/payment-done/'),
        'cancel_return':'http://{}{}'.format(host,'/payment-cancelled/'),
    }
    form=PayPalPaymentsForm(initial=paypal_dict)
    #End of paypal
    return render(request,'checkout.html',{"form":form,"book_dest":book_dest,"cart":user_cart})


@login_required(login_url='/accounts/login/')
@csrf_exempt
def payment_done(request):
    user_cart=Cart.objects.get(user_mac=gma(),ordered=False)
    book_dest=BookedDest.objects.filter(user_mac=gma(),paid=False)
    user_cart.ordered=True
    user_cart.receipt_no=uuid.uuid4().hex[:6].upper()
    user_cart.payment_method="Paypal"
    user_cart.save()

    for dest in book_dest:
        dest.paid=True
        dest.save()
    messages.info(request,'Your booking has been made successfully.Thank you for choosing Travel Agency')
    return redirect('welcome')


@login_required(login_url='/accounts/login/')
@csrf_exempt
def payment_cancelled(request):
    messages.info(request,'Payment has been cancelled successfully')
    return redirect('welcome')


@login_required(login_url='/accounts/login/')
@csrf_exempt
def payment_error(request):
    messages.info(request,'Your payment process incurred an error.Please contact us to report the matter.')
    return redirect('welcome')











    









    


                







    




