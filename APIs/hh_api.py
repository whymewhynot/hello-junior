import requests
import json

employment_status={'Полная занятость' : 'f',
                    'Частичная занятость' : 'p',
                    'Стажировка' : 'i',
                    'Проектная работа' : 'p',
                    'Волонтерство' : 'v'}


def get_job_ids_from_page(page_num=0, job_id_list = []):
    print('page_num= ', page_num)
    url = 'https://api.hh.ru/vacancies'
    headers = {'User-Agent': 'HH-User-Agent'}
    params = {
        'area' : '113',
        'specialization' : '1.221',
        'experience' : 'noExperience',
        'period' : '30',
        'page' : page_num,
        'per_page' : '100',
        'order_by' : 'publication_time'
                }

    r = requests.get(url, headers=headers, params=params)
    r_data = r.content.decode('utf-8')
    python_data = json.loads(r_data)
    r.close()

    while page_num <= 19:
        vacancies = python_data['items']
        job_id_list += [job['id'] for job in vacancies]
        print(f'Получено {len(job_id_list)} id')
        page_num += 1
        get_job_ids_from_page(page_num, job_id_list)
    else:
        return job_id_list

def get_job_info(job_id):
    url = f'https://api.hh.ru/vacancies/{job_id}'
    headers = {'User-Agent': 'HH-User-Agent'}

    r = requests.get(url, headers=headers)
    r_data = r.content.decode('utf-8')
    python_data = json.loads(r_data)
    r.close()

    title = python_data['name']
    city = python_data['area']['name']

    if python_data['salary']:
        salary_from = python_data['salary']['from']
        salary_up_to = python_data['salary']['to']
        currency = python_data['salary']['currency']
    else:
        salary_from = None
        salary_up_to = None
        currency = 'RUR'

    experience = python_data['experience']['name']
    company = python_data['employer']['id']

    published = python_data['published_at']

    type_of_employment = employment_status[python_data['employment']['name']]
    if python_data['schedule']['name'] == 'Удаленная работа':
        remote = True
    else:
        remote = False

    description = python_data['description']
    skills = [skill['name'] for skill in python_data['key_skills']]
    archived = python_data['archived']

    job_info = {'title' : title, 'salary_from' : salary_from, 'salary_up_to' : salary_up_to,
                'salary_currency' : currency, 'experience' : experience, 'archived' : archived,
                'published' : published, 'type_of_employment' : type_of_employment,
                'remote' : remote, 'hh_id' : job_id, 'description' : description}
    employer_id = company

    return job_info, skills, employer_id, city


def get_employer_info(employer_id):
    url = f'https://api.hh.ru/employers/{employer_id}'
    headers = {'User-Agent': 'HH-User-Agent'}

    r = requests.get(url, headers=headers)
    r_data = r.content.decode('utf-8')
    python_data = json.loads(r_data)
    r.close()

    name = python_data['name']

    try:
        logo = python_data['logo_urls']['240']
    except TypeError:
        logo = None

    description = python_data['description']

    try:
        website = python_data['site_url']
    except TypeError:
        website = None

    defaults = {'logo' : logo, 'description' : description, 'website' : website}

    # get_or_create data format:
    return {'name' : name, 'defaults' : {'logo' : logo, 'description' : description, 'website' : website}}