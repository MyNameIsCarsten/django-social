# import Django’s built-in forms module 
from django import forms
# import the Dweet model that you created
from .models import Dweet, some_files, Profile

# create a new class, DweetForm, that inherits from forms.ModelForm
class DweetForm(forms.ModelForm):

    # pass the field that you want the form to render, and you define its type
    body = forms.CharField(
        required=True,

        # adding customizations through a widget 
        # choose the type of input element that Django should use and set it to Textarea
        widget=forms.widgets.Textarea(

            # further customize Textarea
            attrs={
                "placeholder": "Dweet something...",
                "class": "textarea is-success is-medium",
            }
        ),
        # removes the Body text that previously showed up due to a Django default setting that renders the name of a form field as its labe
        label="",
    )


    # create a Meta options class in DweetForm
    # allows you to pass any information that isn’t a field to your form class.
    class Meta:

        # define which model ModelForm should take its information from
        model = Dweet

        # omit our profile
        # format as tuple!
        exclude = ("user", 'likes' )

class some_filesForm(forms.ModelForm):
    class Meta:
        model = some_files
        fields = ('description', 'some_file')
        #fields = ('description', 'some_file', 'file_of_user')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('user_avatar',)

        