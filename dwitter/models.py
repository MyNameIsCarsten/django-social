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

    user_avatar = models.ImageField(upload_to='images/', blank=True)

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


class Dweet(models.Model):
    # user field establishes the model relationship to Django’s built-in User model
    # foreign key relationship: each dweet will be associated with only one user
    # pass "dweets" to related_name: allows you to access the dweet objects from the user side of the relationship through .dweets
    # orphaned dweets should stick around by setting on_delete to models.DO_NOTHING
    user = models.ForeignKey(
        # 'dweets' gives you reverse access to the associated Dweet objects through the User model
        User, related_name="dweets", on_delete=models.DO_NOTHING
    )

    # body field defines your content type
    body = models.CharField(max_length=140)

    # optional image field
    dweet_image = models.ImageField(upload_to='photos', blank=True)

    # created_at field records the date and time when the text-based message is submitted
    # value gets automatically added when a user submits a dweet
    created_at = models.DateTimeField(auto_now_add=True)

    # many-to-many: users can make multiple likes and dweets can have multiple likes
    likes = models.ManyToManyField(User, related_name='dweet_likes')

    # custom string: username, the created date, and the first thirty characters of the message body
    def __str__(self):
        return (
            f"{self.user} "
            f"({self.created_at:%Y-%m-%d %H:%M}): "
            f"{self.body[:30]}..."
        )
    
    # return the number of likes
    def number_of_likes(self):
        return self.likes.count()
    

# file model
class some_files(models.Model):
    user = models.ForeignKey(
        # 'user_files' gives you reverse access to the associated some_files objects through the User model
        User, related_name="user_files", on_delete=models.CASCADE
    )

    description = models.CharField(max_length=255, blank=False)
    some_file = models.FileField(upload_to='some_files')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return (
            f"{self.description} "
            f"({self.uploaded_at:%Y-%m-%d %H:%M}): "
        )
    