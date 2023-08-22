from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Dish, Order, Menu
from .forms import DishForm, OrderForm
from django.http import HttpResponse
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect


@login_required(login_url="/login/")
def home(request):
    available_dishes = Dish.objects.filter(availability=True)
    data = Dish.objects.all()
    if request.user.is_authenticated:
        print("User is authenticated")
    else:
        print("User is not authenticated")
    context = {
        'home': available_dishes
    }
    return render(request, 'index.html',context)


def home1(request):
    data = Dish.objects.all()
    if request.user.is_authenticated:
        print("User is authenticated")
    else:
        print("User is not authenticated")
    context = {
        'home1': data
    }
    return render(request, 'home.html',context)


def register(request):
    if request.method == "POST":
        data = request.POST
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        username = data.get("username")
        password = data.get("password")
        email = data.get("email")
        
        user = User.objects.filter(username = username)
        
        if user.exists():
            messages.info(request, "username already Taken")
            return redirect("/register/")
        
        user_email = User.objects.filter(email = email)
        
        if user_email.exists():
            messages.info(request, "email already Taken")
            return redirect("/register/")
        
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        
        user.set_password(password)
        user.save()
        
        messages.info(request, "Account created successfully")
        
        return redirect("/register/")
    return render(request, 'register.html')




def login_page(request):
    if request.method == "POST":
        data = request.POST
        username = data.get("username")
        password = data.get("password")
        email = data.get("email")
        
        user = User.objects.filter(username = username)
        
        if not user.exists():
            messages.error(request, "Invalid username")
            return redirect("/login/")
        
        user_auth = authenticate(username = username, password = password)
        
        if user_auth is None:
            messages.error(request, "Invalid password")
            return redirect("/login/")
        
        else:
            login(request,user_auth)
            return redirect("/home/")
    
    
    return render(request, 'login.html')

def logout_page(request):
    logout(request)
    return redirect("/login/")





@login_required(login_url="/login/")
def addDish(request):
    if request.method == "POST":
        data = request.POST
        dish_name = data.get("dish_name")
        dish_dis = data.get("dish_dis")
        price = data.get("price")
        availability = True
        dish_image = data.get('dish_image')
        
        
        Dish.objects.create(
                dish_name=dish_name, 
                dish_dis=dish_dis, 
                dish_image=dish_image,
                price=price,
                availability=availability,
            )
        
        return redirect("/dish/")
    
    queryset = Dish.objects.all() 
    
    if request.GET.get('search'):
        queryset = queryset.filter(dish_name__icontains=request.GET.get('search'))
        
    
    context = {'dish': queryset}
        
    return render(request, 'dish.html', context)


@login_required(login_url="/login/")
def update_availability(request, dish_id):
    try:
        dish = Dish.objects.get(pk=dish_id)
        dish.availability = not dish.availability
        dish.save()
        return redirect("dish")
    except Dish.DoesNotExist:
        return HttpResponse("dish")
        


@login_required(login_url="/login/")
def update_dish(request, dish_id):
    queryset = Dish.objects.get(id=dish_id)
    
    if request.method == 'POST':
        form = DishForm(request.POST, request.FILES, instance=queryset)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dish item updated successfully.')
            return redirect('dish')
    else:
        form = DishForm(instance=queryset)
    return render(request, 'update_dish.html', {'form': form, 'item': queryset})    
    
    
    
    # if request.method == "POST":
    #     data = request.POST
    #     dish_name = data.get("dish_name")
    #     dish_dis = data.get("dish_dis")
    #     dish_image = request.FILES.get('dish_image')
        
    #     queryset.dish_name = dish_name
    #     queryset.dish_dis = dish_dis
        
    #     if dish_image:
    #         queryset.dish_image = dish_image
            
    #     queryset.save()
    #     return redirect("/dish/")
     
    # context = {'dish': queryset}
    
    # return render(request, 'update_dish.html', context)





def delete_dish(request, id):
    queryset = Dish.objects.get(id = id)
    queryset.delete()
    return redirect("/dish/")


# def add_to_cart(request, dish_id):
#     if request.method == 'POST':
#         dish = Dish.objects.get(pk=dish_id)

#         # Logic to add the dish to the cart
#         cart = request.session.get('cart', {})
#         cart[dish_id] = cart.get(dish_id, 0) + 1
#         request.session['cart'] = cart

#         messages.success(request, f"{dish.dish_name} added to cart!")  # Add success message
        
#         return redirect('home')  # Redirect back to the menu page

#     return redirect('home')




@login_required(login_url="/login/")
def add_to_cart(request, dish_id):
    dish = Dish.objects.get(pk=dish_id)
    user = request.user
    
    # Create or update the menu entry for the dish in the cart
    menu_item, created = Menu.objects.get_or_create(dish=dish, user=user)
    menu_item.quantity += 1
    menu_item.save()
    
    return redirect('menu')  # Redirect back to the menu page


@login_required(login_url="/login/")
def view_cart(request):
    user = request.user
    cart_items = Menu.objects.filter(user=user, quantity__gt=0)
    total_price = sum(item.dish.price * item.quantity for item in cart_items)
    
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required(login_url="/login/")
def place_order(request):
    user = request.user
    cart_items = Menu.objects.filter(user=user, quantity__gt=0)
    total_price = sum(item.dish.price * item.quantity for item in cart_items)
    
    if request.method == 'POST':
        # Create an order for each dish in the cart
        for item in cart_items:
            Order.objects.create(
                user=user,
                dishes=item.dish,
                quantity=item.quantity,
                total_price=item.dish.price * item.quantity,
                status='received'
            )
            item.quantity = 0  # Clear the quantity in the cart
            item.save()
        
        return redirect('order_history')  # Redirect to order history page
    
    return render(request, 'place_order.html', {'cart_items': cart_items, 'total_price': total_price})




@login_required(login_url="/login/")
def order_history(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-id')
    
    return render(request, 'order_history.html', {'orders': orders})


def serialize_decimal(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

def view_cart(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        total_price = Decimal('0.00') 

        # Handle removal of items from cart
        for dish_id in request.POST.getlist('remove'):
            cart.pop(dish_id, None)
        
        # Handle updating quantities of items in cart
        for dish_id in request.POST.getlist('update'):
            new_quantity = int(request.POST.get(f'quantity_{dish_id}'))
            if new_quantity > 0:
                cart[dish_id] = new_quantity
            else:
                cart.pop(dish_id, None)
        
        # Recalculate total price after updates
        for dish_id, quantity in cart.items():
            dish = Dish.objects.get(pk=dish_id)
            total_price += dish.price * quantity
        
        # Update session data with serialized Decimal values
        request.session['cart'] = {str(dish_id): str(quantity) for dish_id, quantity in cart.items()}
        request.session['total_price'] = str(total_price)
        return redirect('view_cart')

    cart = request.session.get('cart', {})
    total_price = Decimal(request.session.get('total_price', '0.00'))  # Convert total_price back to Decimal
    cart_items = []

    for dish_id, quantity in cart.items():
        dish = Dish.objects.get(pk=dish_id)
        cart_items.append({'dish': dish, 'quantity': int(quantity)})  # Convert quantity back to int

    context = {'cart_items': cart_items, 'total_price': total_price}
    return render(request, 'cart.html', context)