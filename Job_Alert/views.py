from django.shortcuts import render, redirect
from django.views import View
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth.models import User
from fuzzywuzzy import fuzz 

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
            print(profile.avatar)
            if profile.is_complete == False:
                 return redirect('compulsary-profile')
            else:
                 profile = Profile.objects.get(user=request.user)
                 if profile.preferred_job_location.lower() == "all india":
                    filtered_jobs = Job.objects.filter(job_type=profile.preferred_job_type)
                 else:
                    filtered_jobs = Job.objects.filter(
                    job_type=profile.preferred_job_type,
                    location__icontains=profile.preferred_job_location
                )
                 print("Step 1:", filtered_jobs)

                 matched_jobs = []
                 for job in filtered_jobs:
                    print(profile.preferred_job_title.lower())
                    print(job.role.lower())
                    match_score = fuzz.partial_ratio(profile.preferred_job_title.lower(), job.role.lower())
                    print(match_score)
                    if match_score > 60:  
                        matched_jobs.append(job)
                    print(matched_jobs)

                 return render(request, "Job_Alert/home.html", {"profile": profile,
                                                                "Jobs": matched_jobs})


            # return render(request, "Job_Alert/home.html", {"profile": profile})
            

class my_profile(View):
     def get(self, request):
        current_user = request.user
        profile = Profile.objects.get(user=current_user)
        print(profile.avatar)
        return render(request, "Job_Alert/profile.html", {'profile': profile})
     
     def post(self, request):
          pass
     

class edit_profile(View):
        def get(self, request):
            return render(request, "Job_Alert/edit_profile.html")