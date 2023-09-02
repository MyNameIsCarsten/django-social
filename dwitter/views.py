from django.shortcuts import render, redirect, get_object_or_404

# Import our form
from .forms import DweetForm, some_filesForm, ProfileForm

# Import our Dweet and Profile model
from .models import Dweet, Profile, some_files

from django.contrib.auth.models import User

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm

from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin

from django.views import generic

from django.conf import settings
from django.core.files.storage import FileSystemStorage


def base_infos(request):
    id = request.user.id
    obj= get_object_or_404(Profile, id=id) 
    return obj

# pointing the incoming request to base.html and telling Django to render that template
def dashboard(request):
    # Check if the user is logged in
    # if yes, show dashboard with dweets

    if str(request.user) != 'AnonymousUser':
        # fill DweetForm with the data that came in through the POST request
        # 'bound form' or 'unbound form'
        # If request.POST exists we get truthy (or None wile be ignored)
        # If there is no POST request we pass 'None'
        form = DweetForm(request.POST or None)

        obj = base_infos(request)

        #  If a user submits the form with an HTTP POST request, then we want to handle that form data
        if request.method == "POST":

            # Django form objects have a method called .is_valid()
            # compares the submitted data to the expected data defined in the form
            if form.is_valid():

                # prevent committing the entry to the database
                dweet = form.save(commit=False)

                # pick the currently logged-in user object from Django’s request object
                dweet.user = request.user

                # write the information to your database
                dweet.save()

                # send the user back to the same page with a GET request
                # prevents double submissions
                # app_name variable : name keyword argument of a path(), which you defined in your URL configuration
                return redirect("dwitter:dashboard", {'loggedInUser': obj})
            
        # use .filter() on Dweet.objects, which allows you to pick particular dweet objects from the table depending on field lookups
        followed_dweets = Dweet.objects.filter(
            # define the queryset field lookup, which is Django ORM syntax for the main part of an SQL WHERE clause
            # You can follow through database relations with a double-underscore syntax (__) specific to Django ORM
            # access the profile of a user and see whether that profile is in a collection that you’ll pass as the value to your field lookup keyword argument
            # =
            # QuerySet object containing profile objects
            # fetch the relevant profiles from your database:
            # access all profile objects in .follows of the currently logged-in user’s profile
            user__profile__in=request.user.profile.follows.all()
        # sort the dweets in descending order of created_at
        ).order_by("-created_at")

        # passed it to your dashboard template in your context dictionary under the key "form"
        return render(
            request, 
            "dwitter/dashboard.html", 
            # followed_dweets variable contains a QuerySet object of all the dweets of all the profiles the current user follows, ordered by the newest dweet first
            {"form": form, "dweets": followed_dweets, 'loggedInUser': obj},
            )
    # if not, redirect to login page
    else:
        return redirect("dwitter:login")

def profile_list(request):
    obj = base_infos(request)
    # use Django’s object-relational mapper (ORM) to retrieve objects from your profile table
    # store them in profiles
    # get all user profiles except for your own (exclude yourself)
    profiles = Profile.objects.exclude(user=request.user)

    # call to render(), to which you pass a string for the template you want to render 
    # context dictionary that contains profiles
    return render(request, "dwitter/profile_list.html", {"profiles": profiles, 'loggedInUser': obj})

def profile(request, pk):
    obj = base_infos(request)
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
    return render(request, "dwitter/profile.html", {"profile": profile, 'loggedInUser': obj})




def change_password(request):
    obj = base_infos(request)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('dwitter:dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'dwitter/change_password.html', {
        'form': form,
        'loggedInUser': obj
    })



class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    # if not given any, django defaults to registration/password_reset_form.html to render the associated template for the view
    template_name = 'dwitter/password_reset.html'
    # template used for generating the body of the email with the reset password link
    email_template_name = 'dwitter/password_reset_email.html'
    # template used for generating the subject of the email with the reset password link
    subject_template_name = 'dwitter/password_reset_subject.txt'
    # message that will be displayed upon a successful password reset request
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    # If not given any, django defaults to 'password_reset_done' after a successful password request. 
    # But I think it makes sense to just redirect the user to the home page without providing any additional template.
    success_url = reverse_lazy('dwitter:dashboard')


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    # use reverse_lazy to redirect the user to the login page upon successful registration
    # for all generic class-based views the urls are not loaded when the file is imported, 
    # so we have to use the lazy form of reverse to load them later when they're available
    success_url = reverse_lazy("dwitter:login")
    template_name = "registration/signup.html"

'''
def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile =  request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        messages.success(request, f'{filename} was successfully uploaded!')
        return redirect('dwitter:dashboard')
    return render(request, 'dwitter/simple_upload.html')
'''


def model_form_upload(request):
    obj = base_infos(request)
    if request.method == 'POST':
        form = some_filesForm(request.POST, request.FILES)
        if form.is_valid():
            # prevent committing the entry to the database
            user_files = form.save(commit=False)
            # pick the currently logged-in user object from Django’s request object
            user_files.user = request.user
            # write the information to your database
            user_files.save()
            return redirect('dwitter:dashboard')
    else:
        form = some_filesForm()
    return render( request, 'dwitter/model_form_upload.html', {
        'form': form,
        'loggedInUser': obj
    })

'''
class ProfileView(generic.CreateView):
    form_class = ProfileForm
    # use reverse_lazy to redirect the user to the login page upon successful registration
    # for all generic class-based views the urls are not loaded when the file is imported, 
    # so we have to use the lazy form of reverse to load them later when they're available
    success_url = reverse_lazy("dwitter:dashboard")
    template_name = "dwitter/profile_change.html"
'''

    
def profile_edit(request, pk):

    obj = base_infos(request)  


    form = ProfileForm(request.POST or None, instance= obj)
    context= {'form': form, 'profile': obj}
    if request.method == 'POST':
        print(request.POST)
        print(request.FILES['user_avatar'])
        print(obj._meta.fields)
        print(obj.user_avatar)

        if form.is_valid():
            obj= form.save(commit= False)
            obj.user_avatar = request.FILES['user_avatar']

            obj.save()

            messages.success(request, "You successfully updated your profile")

            context= {'form': form, 'profile': obj}

            return render(request, 'dwitter/profile_change.html', context)

        else:
            f=ProfileForm(request.POST or None, instance= obj)
            print(f.errors)
            context= {'form': form,
                        'error': 'The form was not updated successfully.', 
                        'profile': obj}
            return render(request,'dwitter/profile_change.html' , context)
    else:
        return render(request,'dwitter/profile_change.html' , context)
