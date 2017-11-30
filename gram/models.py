from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
import datetime as dt
from random import choice
import string as str

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
    profile_pic = models.ImageField(upload_to = 'photos/',blank=True)


    User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])

    def __str__(self):
        return self.email

    @receiver(post_save, sender=User) #post_save:signal for whenever save event occur
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

def generate_id():
        n = 10
        random = str.ascii_uppercase + str.ascii_lowercase + str.digits
        return ''.join(choice(random) for _ in range(n))

class Posts(models.Model):
    image = models.ImageField(upload_to = 'photos/',blank=True)
    post_date = models.DateTimeField(auto_now_add = True)
    description = models.TextField(max_length=500, blank=True)
    user = models.ForeignKey(User)
    location = models.CharField(max_length=30, blank=True)
    slug = models.SlugField(max_length=10,unique=True, default=generate_id)

    def __str__(self):
        return self.description

    class Meta:
        ordering = ['-post_date']

    def get_absolute_url(self):
        return reverse('posts:view', kwargs={'slug': self.slug})

    @classmethod
    def display_post(cls):
        post = cls.objects.all()
        return post

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

class Like(models.Model):
    posts = models.ForeignKey(Posts, related_name='liked_post')
    user = models.ForeignKey(User, related_name='liker')
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} : {}'.format(self.user, self.posts)
