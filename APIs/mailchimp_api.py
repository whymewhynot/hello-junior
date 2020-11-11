from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError
import os
from datetime import datetime, timedelta

api_key = os.environ.get('MAILCHIMP_API_KEY')

mailchimp = Client()
mailchimp.set_config({
  "api_key": api_key,
  "server": "us2"
})
list_id = os.environ.get('MAILCHIMP_LIST_ID')


def subscribe_or_unsubscribe(email_list):
    members_data = []

    for email in email_list:
        member_email = email["email"]
        members_status = "subscribed" if email["is_subscribed"] else "unsubscribed"
        members_data.append({"email_address" : member_email, "status" : members_status})

    try:
        mailchimp.lists.batch_list_members(list_id, {"members": members_data, "update_existing" : True})
    except ApiClientError as error:
        print(f"Error: {error.text}")



def create_email_template(jobs_data):
    email_template_path = os.path.abspath('email_template.html')

    with open(email_template_path, mode='r', encoding='utf8') as f:
        email_template = f.read()

    jobs_html_list = []
    for job in jobs_data:
        job_str = f'<li><a href="https://hello-junior.herokuapp.com/job/{job["id"]}" target="_blank">{job["title"]}</a></li>'
        jobs_html_list.append(job_str)

    jobs_html_list = '\n'.join(jobs_html_list)

    email_template = email_template.replace('JOBS_CONTENT_BLOCK', jobs_html_list)

    return email_template

def send_newsletter(emails, email_template):

    template_name = datetime.now().strftime('%d.%m.%Y %H:%M:%S')

    template_html = email_template

    from_date = (datetime.now() - timedelta(days=1)).strftime('%d.%m.%Y')
    to_date = datetime.now().strftime('%d.%m')
    template_subject = f"Новые вакансии {from_date}-{to_date}"

    # create new template:
    try:
        repsonse = mailchimp.templates.create({"name": template_name, "html": template_html})
        template_id = repsonse['id']
    except ApiClientError as error:
        print(f"Error: {error.text}")

    # tag subscribers:
    try:
        repsonse = mailchimp.lists.create_segment(list_id, {"name": template_name, "static_segment": emails})
        tag_id = repsonse['id']
    except ApiClientError as error:
        print(f"Error: {error.text}")

    # create campaign:
    try:
        response = mailchimp.campaigns.create({"type": "regular",
                                               "recipients": {
                                                   "segment_opts": {"match": "all", "conditions": [{
                                                       'condition_type': 'StaticSegment',
                                                       'field': 'static_segment',
                                                       'op': 'static_is',
                                                       'value': tag_id
                                                   }]},
                                                   "list_id": list_id
                                               },
                                               "settings": {"subject_line": template_subject,
                                                            "reply_to": "hello-junior@yandex.ru",
                                                            "from_name": "Hello Junior", "template_id": template_id}
                                               })
        campaign_id = response['id']
    except ApiClientError as error:
        print("Error: {}".format(error.text))

    # send campaign:
    try:
        mailchimp.campaigns.send(campaign_id)
    except ApiClientError as error:
        print(f"Error: {error.text}")
