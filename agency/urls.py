from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns=[
    url('^$',views.welcome,name = 'welcome'),
    url(r'^country/(\d+)',views.single_country,name ='country'),
    url(r'^destination/(\d+)',views.single_destination,name ='destination'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('alldest/', views.all_destinations, name='alldest'),
    url(r'^logout/$',views.logout_function,name="logout"),
    url(r'^new/profile$', views.new_profile, name='new_profile'),
    url(r'displayprofile/(\d+)',views.display_profile,name='displayprofile'),
    url(r'^new/review$', views.make_review, name='make_review'),
    path('wishlist/',views.displaywishlist,name='displaywishlist'),
    url(r'addtowishlist/(\d+)',views.addtowishlist,name='addtowishlist'),
    url(r'deletefromwishlist/(\d+)',views.deletefromwishlist,name='deletefromwishlist'),

   
    
]
