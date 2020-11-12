import os, sys
from datetime import datetime, timedelta
from APIs.mailchimp_api import create_email_template, send_newsletter

project_dir = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'hello_junior.settings'

import django
django.setup()

from django.contrib.auth import get_user_model
from jobs.models import Job
from django.utils import timezone

User = get_user_model()

last_day = datetime.now(tz=timezone.utc) - timedelta(days=1)

users_data = []
jobs_data = []

users = User.objects.filter(is_subscribed=True)
if users:
    users_data = [{'email' : user.email,
                   'city' : str(user.city).replace('None', ''),
                   'remote' : user.remote,
                   'skills' : list(user.skills.values_list('name', flat=True))}
                  for user in users]

jobs = Job.objects.filter(published__gte=last_day)

if jobs:
    jobs_data = [{'id' : job.id,
                  'city' : job.city.name,
                  'remote' : job.remote,
                  'skills' : list(job.skills.values_list('name', flat=True))}
                 for job in jobs]

# final_result_format = {
#     'Москва' : {
#         'Python, JavaScript' : {'emails' : [], 'jobs' :[]}
#         }
# }

def list_to_str(skills):
       return ', '.join(skills)

def is_intersect(user_skills, job_skills):
    is_intersect = set(user_skills).intersection(set(job_skills))
    return bool(is_intersect)

def add_or_create(city, skills, job, email):
    try:
        result[city][list_to_str(skills)]['jobs'].add(job)
        result[city][list_to_str(skills)]['emails'].add(email)
    except KeyError:
        result[city] = {list_to_str(skills): {'jobs': set([job]), 'emails': set([email])}}


result = dict()

if jobs_data and users_data:
    remote_jobs = [job['id'] for job in jobs_data if job['remote']][:10]
    result['empty_city'] = {'empty_skills' : {'jobs' : remote_jobs, 'emails' : set()}}


    for user in users_data:
           for job in jobs_data:
                  # user's profile is empty
                  if not user['city'] and not user['skills']:
                         result['empty_city']['empty_skills']['emails'].add(user['email'])

                  # job in user's city
                  if user['city'] == job['city']:
                         if is_intersect(user['skills'], job['skills']):
                                add_or_create(user['city'], user['skills'], job['id'], user['email'])

                  # user is considering remote job
                  if user['city'] and user['remote'] and job['remote']:
                         if is_intersect(user['skills'], job['skills']):
                                add_or_create(user['city'], user['skills'], job['id'], user['email'])

                  # remote job only
                  if not user['city'] and user['remote'] and job['remote']:
                      if is_intersect(user['skills'], job['skills']):
                          add_or_create('remote', user['skills'], job['id'], user['email'])


if result:
    for city_segment in result.values():
        for segment in city_segment.values():
            jobs_segment_data = Job.objects.\
                                filter(id__in=segment['jobs']).\
                                values('id', 'title')[:5]
            jobs_segment_data = list(jobs_segment_data)
            email_template = create_email_template(jobs_segment_data)
            send_newsletter(emails=list(segment['emails']), email_template=email_template)








