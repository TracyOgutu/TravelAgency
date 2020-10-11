from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns=[
    url('^$',views.welcome,name = 'welcome'),
    url(r'^country/(\d+)',views.single_country,name ='country'),
    url(r'^destination/(\d+)',views.single_destination,name ='destination'),
    path('alldest/', views.all_destinations, name='alldest'),
    url(r'^logout/$',views.logout_function,name="logout"),
    url(r'^new/profile$', views.new_profile, name='new_profile'),
    url(r'displayprofile/(\d+)',views.display_profile,name='displayprofile'),
    url(r'^new/review$', views.make_review, name='make_review'),
   
    
]
