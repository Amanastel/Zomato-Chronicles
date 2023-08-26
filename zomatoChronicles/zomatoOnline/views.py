from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Dish, Order, Menu, Cart
from .forms import DishForm, OrderForm, CartForm
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
    
    
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id)

    if request.method == 'POST':
        form = CartForm(request.POST, instance=cart_item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cart item updated successfully.')
            return redirect('view_cart')

    form = CartForm(instance=cart_item)
    context = {'form': form, 'cart_item': cart_item}
    return render(request, 'update_cart_item.html', context)
    
    
def view_cart(request):
    if request.method == 'POST':
        form_id = request.POST.get('form_id')
        form = CartForm(request.POST, prefix=form_id)
        if form.is_valid():
            form.save()
            return redirect('view_cart')

    cart_items = Cart.objects.filter(user=request.user)
    cart_forms = {item.dish.id: CartForm(instance=item, prefix=f'form_{item.id}') for item in cart_items}
    total_price = sum(item.dish.price * item.quantity for item in cart_items)
    
    
    context = {
        'cart_items': cart_items,
        'cart_forms': cart_forms,
        'total_price': total_price,
        # 'oneItemPrice': oneItemPrice
    }

    return render(request, 'cart.html', context)
    
    
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



# @login_required(login_url="/login/")
# def place_order(request):
#     user = request.user
#     cart_items = Menu.objects.filter(user=user, quantity__gt=0)
#     total_price = sum(item.dish.price * item.quantity for item in cart_items)
    
#     if request.method == 'POST':
#         # Create an order for each dish in the cart
#         for item in cart_items:
#             Order.objects.create(
#                 user=user,
#                 dishes=item.dish,
#                 quantity=item.quantity,
#                 total_price=item.dish.price * item.quantity,
#                 status='received'
#             )
#             item.quantity = 0  # Clear the quantity in the cart
#             item.save()
        
#         return redirect('order_history')  # Redirect to order history page
    
#     return render(request, 'place_order.html', {'cart_items': cart_items, 'total_price': total_price})




# @login_required(login_url="/login/")
# def order_history(request):
#     user = request.user
#     orders = Order.objects.filter(user=user).order_by('-id')
    
#     return render(request, 'order_history.html', {'orders': orders})


def serialize_decimal(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


@login_required(login_url="/login/")
def add_to_cart(request, dish_id):
    print("add_to_cart view called")
    dish = Dish.objects.get(pk=dish_id)
    user = request.user

    # Create or update the cart entry for the dish in the user's cart
    cart_item, created = Cart.objects.get_or_create(user=user, dish=dish)
    cart_item.quantity += 1
    cart_item.save()

    return redirect('view_cart')  # Redirect back to the cart page



from django.db.models import Count
from .forms import CartForm  # Import your CartForm class

# @login_required(login_url="/login/")
# def view_cart(request):
#     user = request.user
#     cart_items = Cart.objects.filter(user=user, quantity__gt=0).select_related('dish')
    
#     if request.method == 'POST':
#         cart_forms = [CartForm(request.POST, instance=item) for item in cart_items]
#         if all(form.is_valid() for form in cart_forms):
#             for form in cart_forms:
#                 form.save()
#             return redirect('view_cart')
#     else:
#         cart_forms = [CartForm(instance=item) for item in cart_items]

#     # Calculate the total price
#     total_price = sum(item.dish.price * item.quantity for item in cart_items)
    
#     return render(request, 'cart.html', {'cart_items': cart_items, 'cart_forms': cart_forms, 'total_price': total_price})






@login_required(login_url="/login/")
def place_order(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user, quantity__gt=0).select_related('dish')
    total_price = sum(item.dish.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        # Create order instances and update dish availability
        for cart_item in cart_items:
            Order.objects.create(
                user=user,
                dishes=cart_item.dish,
                quantity=cart_item.quantity,
                total_price=cart_item.dish.price * cart_item.quantity,
                status='received'  # You can set the initial order status here
            )
            # Update dish availability
            cart_item.dish.availability = False
            cart_item.dish.save()

        # Clear the cart
        cart_items.delete()

        messages.success(request, 'Order placed successfully!')
        return redirect('view_cart')

    return render(request, 'place_order.html', {'total_price': total_price})


@login_required(login_url="/login/")
def order_history(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-id')

    return render(request, 'order_history.html', {'orders': orders})