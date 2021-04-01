from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.mail import send_mail, EmailMessage
from django.contrib import messages
from django.http import HttpResponse
User = get_user_model()
from django.contrib.auth.decorators import login_required
from resources.models import Resource
from home.models import Feed

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if email.find("thapar.edu") == -1:
                messages.add_message(request, messages.INFO, f'''Please enter thapar's email id''')
                return redirect('register')
                    
            else:
                User = form.save()
                return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'user/register.html', {'form': form})

def calculate_ratings(id):
    user = User.objects.get(id=id)
    all_ratings = Rating.objects.filter(rating_of=user)
    n = all_ratings.count()
    total_ratings = 0
    if(n==0):
        n = 1

    for obj in all_ratings:
        total_ratings += obj.ratings
    
    ratings = round(total_ratings/n, 1)

    return ratings


@login_required
def user_profile_resources(request, pk):
    user = User.objects.get(id=pk)
    if(request.method == 'POST'):
        form = RatingsForm(request.POST)
        if form.is_valid():
            form.save()
            form.instance.rating_of = user
            form.instance.rated_by = request.user
            form.save()
            user.ratings = calculate_ratings(pk)
            user.save()

    feeds = Feed.objects.filter(author=user)
    resources = Resource.objects.filter(owner=user)
    context = {
        'form' : RatingsForm(),
        'user' : user,
        'resources' : resources,
        'feeds' : feeds,
    }

    return render(request, 'user/user_profile.html', context)



