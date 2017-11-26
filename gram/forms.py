from django import forms
from .models import Profile,Posts
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('website', 'bio', 'location', 'phone_number')

class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ('image','description')
