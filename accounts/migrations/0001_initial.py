# Generated by Django 3.1.2 on 2020-11-11 11:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='Email')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_subscribed', models.BooleanField(default=True, verbose_name='Подписка на рассылку')),
                ('registered', models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Последнее обновление')),
                ('remote', models.BooleanField(blank=True, default=False, null=True, verbose_name='Удалённая работа')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='jobs.city', verbose_name='Город')),
                ('favorites', models.ManyToManyField(null=True, to='jobs.Job')),
                ('skills', models.ManyToManyField(blank=True, null=True, to='jobs.Skill', verbose_name='Навыки')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
                'db_table': 'auth_user',
            },
        ),
    ]
