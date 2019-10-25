from django.conf import settings
from django.templatetags.static import static
from django.shortcuts import render, redirect, render_to_response, HttpResponseRedirect
from django.http import HttpResponse, Http404
import datetime as dt
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib import messages


# Create your views here.

def index(request):
    date = dt.date.today()
    business = Business.get_allbusiness()
    # neighborhood = request.GET['']
    # business_location = Business.get_by_neighborhood(neighborhood)
    if 'neighborhood' in request.GET and request.GET["neighborhood"]:
        neighborhoods = request.GET.get("neighborhood")
        searched_neighborhood = Business.get_by_neighborhood(neighborhoods)
        message = f"{neighborhoods}"

        return render(request, 'index.html', {"message":message,"location": searched_neighborhood})

    else:
        message = "No Neighborhood Found!"

    return render(request, 'index.html', {"date": date, "business":business})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('/')
        
    else:
        form = RegisterForm()
    return render(request, 'registration/registration_form.html', {'form':form})
    
    
@login_required(login_url='/accounts/login/')
def search_businesses(request):
    if 'keyword' in request.GET and request.GET["keyword"]:
        search_term = request.GET.get("keyword")
        searched_projects = Business.search_business(search_term)
        message = f"{search_term}"

        return render(request, 'search.html', {"message":message,"projects": searched_projects})

    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html', {"message": message})


def get_business(request, id):

    try:
        project = Business.objects.get(pk = id)
        
    except ObjectDoesNotExist:
        raise Http404()
    
    
    return render(request, "projects.html", {"project":project})
  

@login_required(login_url='/accounts/login/')
def new_business(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewBusinessForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.Author = current_user
            project.save()
        return redirect('index')

    else:
        form = NewBusinessForm()
    return render(request, 'new-business.html', {"form": form})


@login_required(login_url='/accounts/login/')
def user_profiles(request):
    current_user = request.user
    profile = request.user.profile
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        form2 = NewNeighborhoodForm(request.POST)
        
        if form2.is_valid():
            neighborhood = form2.save(commit=False)
            neighborhood.Admin = current_user
            neighborhood.admin_profile = profile
            neighborhood.save()
            return redirect('profile')
        
        if form.is_valid():
            profile = form.save(commit=False)
            profile.save()
            print("*********** Form 1")
            return redirect('profile')
            
    else:
        form = ProfileUpdateForm()
        form2 = NewNeighborhoodForm()

    return render(request, 'registration/profile.html', {"form":form, "form2":form2})

