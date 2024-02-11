from django.shortcuts import render

from.models import *
# Create your views here.
def home(request):
    return render(request,"store/index.html")

def collections(request):
    category= Category.objects.filter(status=0)
    
    return render(request,"store/collections.html",{'category':category})   