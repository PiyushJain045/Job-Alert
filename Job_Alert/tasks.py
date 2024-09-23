# job_alert/tasks.py
from celery import shared_task
from .models import Job, Profile
from django.core.mail import send_mail
from django.conf import settings
from fuzzywuzzy import fuzz 

@shared_task(bind=True)
def check_job_match_and_notify_users(self, job_id):
    print("inside celery task")
    try:
        job = Job.objects.get(id=job_id)
        # Fetch all profiles that match job criteria
        profiles = Profile.objects.filter(
            preferred_job_type=job.job_type
        )
        print("Profile:", Profile)

        matched_profiles = []
        for profile in profiles:
            print("Inside loop")
            if profile.preferred_job_location.lower() == "all india" or job.location.lower() in profile.preferred_job_location.lower():
                match_score = fuzz.partial_ratio(profile.preferred_job_title.lower(), job.role.lower())
                print("match score:", match_score)
                if match_score > 60:
                    matched_profiles.append(profile)
        print("matched_profile:", matched_profiles)

        # Notify matched profiles
        for profile in matched_profiles:
            print("Insode mail loop")
            print("Profile:",profile)
            print(profile.user.email)
            send_mail(
                subject='New Job Matching Your Preferences!',
                message=f'Hi {profile.user.username},\n\nA new job "{job.role}" at {job.company_name} matches your preferences. Check it out: {job.link_to_original_source}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[profile.user.email],
                fail_silently=False,
            )

        print(f"Notifications sent to {len(matched_profiles)} users.")
    except Job.DoesNotExist:
        print("Job does not exist.")
