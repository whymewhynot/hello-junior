from APIs.mailchimp_api import subscribe_or_unsubscribe
from datetime import datetime, timedelta

import os, sys

project_dir = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'hello_junior.settings'

import django
django.setup()
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Q


last_day = datetime.now(tz=timezone.utc) - timedelta(days=1)

User = get_user_model()

users = User.objects.filter(
    Q (registered__gte=last_day, is_subscribed=True) |
    Q (updated__gte=last_day)
                            ).values('email', 'is_subscribed')

users = list(users)

if users:
    subscribe_or_unsubscribe(users)