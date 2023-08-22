from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Dish, Menu, Order

class YourAppTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_home_view(self):
        response = self.client.get('/home/')  # Replace with your URL
        self.assertEqual(response.status_code, 200)
    
    def test_login_view(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, 302)  # Expecting a redirect after successful login
        self.assertRedirects(response, reverse('home'))  # Assuming the home view is redirected to
    
    # def test_dish_model_str(self):
    #     dish = Dish.objects.create(dish_name='Test Dish')
    #     self.assertEqual(str(dish), 'Test Dish')

    def test_menu_model_str(self):
        dish = Dish.objects.create(dish_name='Test Dish')
        menu = Menu.objects.create(user=self.user, dish=dish, quantity=3)
        self.assertEqual(str(menu), 'Test Dish - Quantity: 3')

    def test_order_model_str(self):
        dish = Dish.objects.create(dish_name='Test Dish')
        order = Order.objects.create(user=self.user, dishes=dish, quantity=1, total_price=10, status='received')
        self.assertEqual(str(order), 'Order for testuser - Test Dish - received')

    def test_dish_model_str(self):
        dish = Dish.objects.create(dish_name='Test Dish', price=10.0)  # Provide a valid price
        self.assertEqual(str(dish), 'Test Dish')