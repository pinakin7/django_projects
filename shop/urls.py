from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name='Shop Home'),
    path('about/',views.about,name=' About Us '),
    path('contact/',views.contact,name=' Contact Us '),
    path('track/',views.track,name=' Track Order '),
    path('search/',views.search,name=' Search '),
    path('productview/<int:myid>',views.productview,name=' Product View '),
    path('checkout/',views.checkout,name=' Checkout '),
    # path('handlepayment/',views.handle_payment,name=' Handle Payment '),

]
