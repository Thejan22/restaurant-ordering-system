from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages

def register(request):
     # Check if the form is submitted (POST request)
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Account created successfully! Welcome, {user.username}!")
            return redirect('menu')
    else:
         # If GET request, create an empty registration form
        form = UserCreationForm()
    # Render the registration template with the form
    return render(request, 'accounts/register.html', {'form': form})
