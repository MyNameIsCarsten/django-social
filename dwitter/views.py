from django.shortcuts import render
from .models import Profile

# pointing the incoming request to base.html and telling Django to render that template
def dashboard(request):
    return render(request, "base.html")

def profile_list(request):
    # use Django’s object-relational mapper (ORM) to retrieve objects from your profile table
    # store them in profiles
    # get all user profiles except for your own (exclude yourself)
    profiles = Profile.objects.exclude(user=request.user)

    # call to render(), to which you pass a string for the template you want to render 
    # context dictionary that contains profiles
    return render(request, "dwitter/profile_list.html", {"profiles": profiles})

def profile(request, pk):
    # pick a specific profile by its primary key ID
    profile = Profile.objects.get(pk=pk)
    return render(request, "dwitter/profile.html", {"profile": profile})