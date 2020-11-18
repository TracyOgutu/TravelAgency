from django.contrib import admin
from .models import Destination,Package,Country,Subscribe,Cart,BookedDest

# Register your models here.
admin.site.register(Country)
admin.site.register(Destination)
admin.site.register(Package)
admin.site.register(Subscribe)
admin.site.register(Cart)
admin.site.register(BookedDest)

