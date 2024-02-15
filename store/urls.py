from django.urls import path
from.import views

urlpatterns = [
    path('',views.home,name='home'),
    path('menu/<str:slug>',views.menu,name='menu'),
    path('restaurant',views.restaurant,name='restaurant'),
    path('login/',views.login,name="login"),
    path('logout/',views.logout, name='logout'),
	path('signup/',views.signup,name='signup'),
    path('cart/', views.view_cart, name='view_cart'),
    path('place_order/',views.place_order, name='place_order'),
	path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
	path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
	path('add_quantity/<int:item_id>/', views.add_quantity, name='add_quantity'),
	path('subtract_quantity/<int:item_id>/', views.subtract_quantity, name='subtract_quantity'),
    path('order_success/', views.order_success, name='order_success'),
	path('view_products/', views.view_products, name='view_products'),
    path('pay_homepage/', views.pay_homepage, name='pay_homepage'),

    
    
]