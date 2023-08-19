from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Dish, Menu, Order



class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ['dish_name', 'price', 'availability', 'dish_dis', 'dish_image']
        
        
class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['quantity']
        
        
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['dishes', 'status']