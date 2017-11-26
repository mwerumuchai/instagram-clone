from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
import datetime as dt
# genders = (
#     ('male','Male'),
#     ('female' 'Female'),
#     ('not_specified' 'Not Specified'),
# )

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.CharField(max_length=30, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    email = models.EmailField()
    phone_number = PhoneNumberField(max_length=10, blank=True)
    # gender = models.CharField(max_length=25,choices=genders)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateTimeField(null=True, blank=True)

    @receiver(post_save, sender=User) #post_save:signal for whenever save event occur
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

class Posts(models.Model):
    image = models.ImageField(upload_to = 'photos/',blank=True,)
    profile = models.ForeignKey(Profile,blank=True, null=True)
    post_date = models.DateTimeField(auto_now_add = True)
    description = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.profile

    class Meta:
        ordering = ['-post_date']

    @classmethod
    def display_post(cls):
        post = Posts.objects.all()
        return post


class Comments(models.Model):
    comment = models.TextField(max_length=255, blank=True)
    posts = models.ForeignKey(Posts)
    user = models.ForeignKey(User)
    pub_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.comment
