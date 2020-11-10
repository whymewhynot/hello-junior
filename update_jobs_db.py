import os, sys

project_dir = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'hello_junior.settings'

import django
django.setup()

from APIs.hh_api import get_job_ids_from_page, get_job_info, get_employer_info
from jobs.models import Job, City, Employer, Skill


def save_job(job_info, skills, employer_info, city):

    employer, _ = Employer.objects.get_or_create(**employer_info)
    job_info['company'] = employer
    job_info['city'], _ = City.objects.get_or_create(name=city)

    job_db = Job(**job_info)
    try:
        job_db.save()
        print(f"Job {job_info['hh_id']} is added")
    except Exception as e:
        print(f"Error while job {job_info['hh_id']} adding: {e}")

    employer.vacancies.add(job_db)
    print(f"Employer {employer}: job {job_info['hh_id']} is added")

    if skills:
        for i in skills:
            skill, _ = Skill.objects.get_or_create(name=i)
            job_db.skills.add(skill)
            print(f"Skill {skill} is added")



db_id_list = list(Job.objects.filter(archived=False).values_list('hh_id', flat=True))
hh_id_list = get_job_ids_from_page(page_num=18)

new_ids_list = list(set(hh_id_list) - set(db_id_list))
mb_old_ids_list = list(set(db_id_list) - set(hh_id_list))

print(f'Number of new jobs: {len(new_ids_list)}')
print(f'Number of maybe_old_jobs: {len(mb_old_ids_list)}')

if new_ids_list:
    for id in new_ids_list:
        job_info, skills, employer_id, city = get_job_info(id)
        employer_info = get_employer_info(employer_id)
        save_job(job_info, skills, employer_info, city)

if mb_old_ids_list:
    for id in mb_old_ids_list:
        job_info, skills, employer_id, city = get_job_info(id)
        if job_info['archived']:
            Job.objects.filter(hh_id=id).update(archived=True)



