from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm
from .models import CustomUser

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in.
            CustomUser.objects.create(
                user=user,
                name=form.cleaned_data['username'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address']
                
            )
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            auth = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')  # Replace 'home' with the appropriate URL name
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
