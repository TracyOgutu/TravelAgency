from django.contrib import admin
from .models import Destination,Package,Country,Subscribe

# Register your models here.
admin.site.register(Country)
admin.site.register(Destination)
admin.site.register(Package)
admin.site.register(Subscribe)

