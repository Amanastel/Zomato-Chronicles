from django.contrib.auth.models import User
from django.db import models



class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=13)
    address = models.CharField(max_length=255)
    
    @property
    def username(self):
        return self.user.username

    def __str__(self):
        return self.username

class Dish(models.Model):
    dish_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    availability = models.BooleanField(default=True)
    def __str__(self):
        return self.dish_name

class Menu(models.Model):
    dish = models.OneToOneField(Dish, on_delete=models.CASCADE, primary_key=True)
    quantity = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.dish.dish_name} - Quantity: {self.quantity}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dishes = models.ManyToManyField(Dish)
    status_choices = (
        ('received', 'Received'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready for Pickup'),
        ('delivered', 'Delivered')
    )
    status = models.CharField(max_length=20, choices=status_choices, default='received')
    
    def __str__(self):
        return f"Order for {self.user.username} - Status: {self.get_status_display()}"