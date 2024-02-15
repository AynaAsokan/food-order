from django.shortcuts import render,redirect
from django.contrib.auth import login as authlogin,logout as authlogout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from.models import *
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
# Create your views here.

def home(request):
    if request.user.is_authenticated == True:
                username=request.user.username
    else:
                username = None  
    return render(request,"home.html",{'username':username})

def menu(request,slug):
    if(Category.objects.filter(slug=slug)):
        food=Product.objects.filter(category__slug=slug)
        category_name=Category.objects.filter(slug=slug).first()
    
    return render(request,"menu.html",{"food":food,"category_name":category_name})

def restaurant(request):
    restaurant=Category.objects.all()
    return render(request,"restaurant.html",{"restaurant":restaurant})    


def view_cart(request):
        cart_items = CartItem.objects.filter(user=request.user)
        print(cart_items)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required(login_url='login')
def add_to_cart(request, product_id):
        product = Product.objects.get(id=product_id)
        cart_item,created = CartItem.objects.get_or_create(product=product,user=request.user)
        cart_item.quantity += 1
        cart_item.save()
        return redirect('view_cart')  

        

def remove_from_cart(request, item_id):
	cart_item = CartItem.objects.get(id=item_id)
	cart_item.delete()
	return redirect('view_cart') 

def add_quantity(request, item_id):
	cart_item = CartItem.objects.get(id=item_id)
	cart_item.quantity += 1
	cart_item.save()
	return redirect('view_cart') 

def subtract_quantity(request, item_id):
	cart_item = CartItem.objects.get(id=item_id)
	cart_item.quantity -= 1
	cart_item.save()
	if cart_item.quantity == 0:
	   cart_item.delete()
	return redirect('view_cart') 



def place_order(request):
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        for item in cart_items:
              item.total_price=total_price
              item.save()
        return render(request, 'place_order.html', { 'total_price': total_price})    

def about(request):
    return render(request,'about.html')
def registration(request):
    # accounts/views.py
    form=RegistrationForm(request.POST or None)
    if form.is_valid():
        form.save()
    return render(request, 'registration.html', {'form': form})

    




def login(request):
	error_message=None
	if request.POST:
            username=request.POST['Username']
            password=request.POST['Password']
            user=authenticate(username=username,password=password)
            if user:
		            authlogin(request,user)
		            return redirect('home')
            else:
		            error_message='invalid credentials'	
	return render(request,'loginuser.html',{'error_message':error_message})



def logout(request):
	authlogout(request)
	return redirect('home')




def signup(request):
    user = None
    error_message =None
    if request.POST:
	    username=request.POST['Username']
	    password=request.POST['Password']
	    try:
	        user= User.objects.create_user(username=username,password=password)
	    except Exception as e:
		       error_message=str(e)		 
    return render(request,'signup.html',{'user': user, 'error_message':error_message})

@csrf_exempt
def order_success(request):
	return render(request,'order_success.html')


def view_products(request):
        if request.user.is_authenticated == True:
                username=request.user.username
        else:
                username = None    
        
        cartitem=CartItem.objects.filter(user=request.user)
        for items in cartitem:
            total_price=items.total_price

        
        return render(request, 'view_products.html', {'cartitem': cartitem,'total_price':total_price,'username':username})    


def pay_homepage(request):
    if request.method == 'POST': 
        client=None
        address = request.POST.get('address')
        pincode=request.POST.get('pincode')
        mobile=request.POST.get('mobile')
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        for item in cart_items:
              item.total_price=total_price
              item.save()
              amount=100
        client = razorpay.Client(auth=("rzp_test_fTUneBnC7XgBlC", "wysvSDVz748OyUF5UDiQtTdA"))
        payment = client.order.create({'amount':amount,'currency': 'INR','payment_capture':'1'})	

    return render(request,'pay_homepage.html',{'total_price':total_price,'address':address,'pincode':pincode,'mobile':mobile})

