from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


@login_required(login_url='/accounts/login/')
def index(request):
    return render(request, 'index.html')

@login_required(login_url='/accounts/register/')
def homepage(request):
    return render(request, 'homepage.html')

def logout(request):
    return render(request, 'index.html')
