from __future__ import absolute_import
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction
from django.http import Http404
from .forms import UserForm,ProfileForm,PostForm,ProfilePicForm,NewCommentsForm
from .models import Posts, Like, Profile, Follow, Comments
import datetime as dt
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from vote.managers import VotableManager

#votes
votes = VotableManager()


@login_required(login_url='/accounts/register/')
def index(request):
    current_user = request.user
    post = Posts.get_posts()

    # follow other users
    return render(request, 'index.html',{"post":post,"user":current_user})

@login_required(login_url='/accounts/login/')
def homepage(request):
    return render(request, 'homepage.html')

def logout(request):
    return render(request, 'index.html')

@login_required
@transaction.atomic
def update_profile(request,username):
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
def posts(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST,files =request.FILES)
        if post_form.is_valid():
            single_post = Posts(user =request.user ,image = request.FILES['image'], description = request.POST['description'] )
            single_post.save()
            messages.success(request, ('Your post was successfully updated!'))
            return redirect(reverse('profiles', kwargs = {'username': request.user.username}))
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



# like/upvote post
@login_required (login_url='/accounts/register/')
def upvote_posts(request, pk):
    post = Posts.get_single_post(pk)
    user = request.user
    user_id = user.id

    if user.is_authenticated:
        upvote = post.votes.up(user_id)
        print(upvote)
        post.upvote_count = post.votes.count()
        post.save()
    return redirect('home')

# dislike/downvote post
@login_required (login_url='/accounts/register/')
def downvote_posts(request, pk):
    post = Posts.get_single_post(pk)
    user = request.user
    user_id = user.id

    if user.is_authenticated:
        downvote = post.votes.down(user_id)
        print(post.id)
        print(downvote)
        print(post.vote_score)
        post.downvote_count = post.votes.count()
        post.save()

    return redirect('home')

# follow
@login_required (login_url='/accounts/register/')
def follow(request,pk):
    current_user = request.user
    follow_profile = Profile.objects.get(pk)
    following = Follow(user=current_user, profile=follow_profile)
    following.save()
    return redirect('follow')


# comment section
@login_required (login_url='/accounts/register/')
def comment(request,pk):
    current_user = request.user
    post = Posts.get_single_post(pk)
    comments = Comments.get_post_comment(post.id)
    form = NewCommentsForm(request.POST)
    if request.method == 'POST':
        if form.is_valid:
            comment = form.save(commit=False)
            comment.user = current_user
            comment.post = post
            comment.image_id = post.id
            comment.save()
            return redirect('home')
        else:
            form = NewCommentsForm()
    return render(request, 'comments/new_comment.html', {"form":form, "post":post, "comments":comments})
