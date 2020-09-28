from django.contrib import admin
from .models import Destination,Package,Country

# Register your models here.
admin.site.register(Country)
admin.site.register(Destination)
admin.site.register(Package)

