from django import forms
from .models import Profile,Posts,Comments
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('profile_pic','website', 'bio', 'location', 'phone_number')

class ProfilePicForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('profile_pic',)

class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ('image','description')

class NewCommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('comment',)
