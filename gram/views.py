from __future__ import absolute_import
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.db import transaction
from .forms import UserForm,ProfileForm,PostForm
from .models import Posts, Like
import datetime as dt


@login_required(login_url='/accounts/login/')
def index(request):
    return render(request, 'index.html')

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
def profile(request):
    # user = User.objects.get(pk=user_id)
    post = Posts.display_post()
    return render(request, 'profiles/profile.html', {"post":post})

@login_required
def posts(request):
    current_user = request.user
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            single_post = post_form.save(commit = False)
            single_post.user = current_user
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
# like post
@login_required
def like_post_view(request, *args, **kwargs):
    try:
        post = Post.objects.get()

        _, created = Like.objects.get_or_create(post=post, user=request.user)

        if not created:
            messages.warning(
                request,
                'You\'ve already liked the post.'
            )
    except Post.DoesNotExist:
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
