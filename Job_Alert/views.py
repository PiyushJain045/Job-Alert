from django.shortcuts import render, redirect
from django.views import View
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth.models import User

from django.contrib.auth.models import User
# Create your views here.


class compulsary_profile(View):
    def get(self, request):
        form = ProfileForm()
        return render(request, "Job_Alert/compulsary_profile.html", {'form': form})
    
    def post(self, request):
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)  # Pass the user to the form
        if form.is_valid():
            profile = form.save(commit=False)  # Prevent saving immediately
            profile.is_complete = True
            profile.save()  # Save the profile
            return redirect('home')  # Redirect after successful submission
        return render(request, "Job_Alert/compulsary_profile.html", {'form': form}) 
    

class home(View):
    def get(self, request):
            current_user = request.user
            profile = Profile.objects.get(user=current_user)
            print(profile.is_complete)
            if profile.is_complete == False:
                 return redirect('compulsary-profile')
            else:
                 profile = Profile.objects.get(user=request.user)
                 return render(request, "Job_Alert/home.html", {"profile": profile})
            

class my_profile(View):
     def get(self, request):
        current_user = request.user
        profile = Profile.objects.get(user=current_user)
        return render(request, "Job_Alert/profile.html", {'profile': profile})
     
     def post(self, request):
          pass
     

class edit_profile(View):
        def get(self, request):
            return render(request, "Job_Alert/edit_profile.html")