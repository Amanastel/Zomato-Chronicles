from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Dish
from .forms import DishForm
from django.http import HttpResponse


@login_required(login_url="/login/")
def home(request):
    data = Dish.objects.all()
    if request.user.is_authenticated:
        print("User is authenticated")
    else:
        print("User is not authenticated")
    context = {
        'home': data
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