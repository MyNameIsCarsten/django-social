# This imports the core models module from Django, which provides classes for defining database models
from django.db import models

# This imports the built-in User model from Django's authentication system, which will be extended to include a profile
from django.contrib.auth.models import User

# This imports the post_save signal, which is emitted after a model's save method is called.
from django.db.models.signals import post_save

# This imports the receiver decorator, used to create a signal receiver function
from django.dispatch import receiver

#defines a custom model named Profile that inherits from Django's models.Model
class Profile(models.Model):

    # creates a one-to-one relationship field named user
    # links the Profile model to the built-in User model
    # on_delete parameter specifies that when a User is deleted, the associated Profile should also be deleted
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # creates a many-to-many relationship field within the Profile model
    follows = models.ManyToManyField(
        "self",
        # access data entries from the other end of the relationship
        related_name="followed_by",
        # users can follow someone without them following back
        symmetrical=False,
        # users don’t need to follow anyone
        blank=True
    )

    # overloaded the default .__str__() method so that it 
    # returns the value of username from the associated instance of the User model
    def __str__(self):
        return self.user.username
 
# signal receiver decorator
# connects the create_profile function to the post_save signal emitted by the User model
@receiver(post_save, sender=User)

# function is triggered whenever a User model is saved
def create_profile(sender, instance, created, **kwargs):

    # checks if a new User instance was created
    if created:
        # creates a Profile instance associated with the new User instance
        # effectively creating a profile for each new user
        user_profile = Profile(user=instance)
        user_profile.save()

        # attempts to set the initial follow relationship for the user's profile to itself
        user_profile.follows.set([instance.profile.id])

        # user_profile instance is saved to the database
        user_profile.save()

