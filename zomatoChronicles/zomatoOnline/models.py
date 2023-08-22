from django.contrib.auth.models import User
from django.db import models



class Dish(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    dish_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    availability = models.BooleanField(default=True)
    dish_dis = models.TextField()
    # dish_image = models.ImageField(upload_to='dish_pic')
    dish_image = models.URLField()
    def __str__(self):
        return self.dish_name

class Menu(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dish = models.OneToOneField(Dish, on_delete=models.CASCADE, primary_key=True)
    quantity = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.dish.dish_name} - Quantity: {self.quantity}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dishes = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status_choices = (
        ('received', 'Received'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready for Pickup'),
        ('delivered', 'Delivered')
    )
    status = models.CharField(max_length=20, choices=status_choices, default='pending')
    
    def __str__(self):
        return f"Order for {self.user.username} - {self.dishes.dish_name} - {self.status}"