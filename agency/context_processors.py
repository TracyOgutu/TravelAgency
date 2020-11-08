from .models import Destination

def destinations(request):
    return {'destinations': Destination.objects.all()}