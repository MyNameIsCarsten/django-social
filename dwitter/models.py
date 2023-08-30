from django.db import models

# import the built-in User model that we want to extend
from django.contrib.auth.models import User

# import post_save
from django.db.models.signals import post_save

# import receiver
from django.dispatch import receiver

class Profile(models.Model):
    # define a OneToOneField object called user
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # define a ManyToManyField object with the field name follows
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
 
# apply the receiver decorator to create_profile
# passing it post_save and passing the User model to sender
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    # ceated is provided by post_save
    if created:
        # associate a profile with a user
        user_profile = Profile(user=instance)
        user_profile.save()
        # add the profile associated with your new user account to the list of accounts that the user is following
        user_profile.follows.set([instance.profile.id])
        # commit the new profile to your database
        user_profile.save()

