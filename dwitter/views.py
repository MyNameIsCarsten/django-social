from django.shortcuts import render
from .models import Profile

# pointing the incoming request to base.html and telling Django to render that template
def dashboard(request):
    return render(request, "dwitter/dashboard.html")

def profile_list(request):
    # use Django’s object-relational mapper (ORM) to retrieve objects from your profile table
    # store them in profiles
    # get all user profiles except for your own (exclude yourself)
    profiles = Profile.objects.exclude(user=request.user)

    # call to render(), to which you pass a string for the template you want to render 
    # context dictionary that contains profiles
    return render(request, "dwitter/profile_list.html", {"profiles": profiles})

def profile(request, pk):

    # in case you haven’t created profiles for you and your existing users
    # verify that your user has a profile in your profile view:
    # check whether request.user contains profile
    if not hasattr(request.user, 'profile'):
            # if the profile is missing, then you create a profile for your user before proceeding
            missing_profile = Profile(user=request.user)
            missing_profile.save()

    # pick a specific profile by its primary key ID
    profile = Profile.objects.get(pk=pk)

    # see whether the incoming request to your Django view function is an HTTP POST reques
    if request.method == "POST":

        # user attribute from Django’s request object, which refers to the currently logged-in user
        # access that user’s .profile object
        # assign it to current_user_profile
        current_user_profile = request.user.profile

        # get the user-submitted data from the request.POST
        data = request.POST

        # accessing the data at the key "follow"
        action = data.get("follow")

        #  either adds or removes the user profile from the currently logged-in user’s .follows
        if action == "follow":
            current_user_profile.follows.add(profile)
        elif action == "unfollow":
            current_user_profile.follows.remove(profile)

        #propagate the changes to .follows back to the database
        current_user_profile.save()
    return render(request, "dwitter/profile.html", {"profile": profile})