"""
URL configuration for zomatoChronicles project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views
from zomatoOnline.views import *

urlpatterns = [
    path('',views.home,name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('home/', home, name='home'),
    path('dish/', addDish, name='dish'),
    path('update_availability/<int:dish_id>/', views.update_availability, name='update_availability'),
    path('update_dish/<int:dish_id>/', views.update_dish, name='update_dish'),
    path('delete-dish/<int:id>/', views.delete_dish, name='delete_dish'),
    # path('order/<int:dish_id>/', views.order_dish, name='order_dish'),
    # path('add_to_cart/<int:dish_id>/', views.add_to_cart, name='add_to_cart'),
    path('view-cart/', views.view_cart, name='view_cart'),
    path('register/', views.register, name='register'),
    # path('order/', views.order_dish, name='order_dish'),
    
    
    
    path('add_to_cart/<int:dish_id>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('place_order/', views.place_order, name='place_order'),
    path('order_history/', views.order_history, name='order_history'),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)