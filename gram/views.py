from __future__ import absolute_import
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction
from django.http import Http404
from .forms import UserForm,ProfileForm,PostForm,ProfilePicForm
from .models import Posts, Like, Profile
import datetime as dt
from django.core.exceptions import ObjectDoesNotExist


@login_required(login_url='/accounts/login/')
def index(request):
    post = Posts.objects.all()
    return render(request, 'index.html',{"post":post})

@login_required(login_url='/accounts/register/')
def homepage(request):
    return render(request, 'homepage.html')

def logout(request):
    return render(request, 'index.html')

@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return redirect('home')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profiles/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def profile(request,username):
    try:
        user = User.objects.get(username=username)
        profile_pic = Profile.objects.filter(user_id=user).all().order_by('-id')
        post = Posts.objects.filter(user_id=user).all().order_by('-id')
    except ObjectDoesNotExist:
        raise Http404()

    return render(request, 'profiles/profile.html', {"post":post, "user":user, "profile_pic":profile_pic})

@login_required
def posts(request,username):
    current_user = request.user.username
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            single_post = post_form.save(commit = False)
            single_post.save()
            messages.success(request, ('Your post was successfully updated!'))
            return redirect('profiles')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        post_form = PostForm()
    return render(request,'profiles/post.html', {
        'post_form': post_form
    })

# update profile pic
def profile_pic_update(request, username):
    current_user = request.user
    if request.method == 'POST':
        form = ProfilePicForm(request.POST, files=request.FILES)
        if form.is_valid():
            single_profile = form.save(commit = False)
            single_profile.user = current_user
            single_profile.save()
            return redirect(reverse('profile', kwargs={'username': request.user.username}))
    else:
        form = ProfilePicForm()
        return render(request,'profiles/update_profilepic.html', {'form':form})



# like post
@login_required
def like_post_view(request, *args, **kwargs):
    try:
        post = Posts.objects.get(slug=kwargs['slug'])

        _, created = Like.objects.get_or_create(post=post, user=request.user)

        if not created:
            messages.warning(
                request,
                'You\'ve already liked the post.'
            )
    except Posts.DoesNotExist:
        messages.warning(
            request,
            'Post does not exist'
        )

    return HttpResponseRedirect(
        reverse_lazy(
            'posts:view',
            kwargs={'slug': kwargs['slug']}
        )
    )
# unlike posts
@login_required
def unlike_post_view(request, *args, **kwargs):
    try:
        like = Like.objects.get(
            post__slug=kwargs['slug'],
            user=request.user
        )
    except Like.DoesNotExist:
        messages.warning(
            request,
            'You didn\'t like the post.'
        )
    else:
        like.delete()

    return HttpResponseRedirect(
        reverse_lazy(
            'posts:view',
            kwargs={'slug': kwargs['slug']}
        )
    )
