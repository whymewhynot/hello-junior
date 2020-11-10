from django.db import models
from django.contrib.humanize.templatetags.humanize import intcomma

class Job(models.Model):
    title = models.CharField(max_length=300, unique=False, verbose_name='Заголовок', blank=True)

    salary_from = models.IntegerField(null=True, blank=True, verbose_name='Зарплата от')
    salary_up_to = models.IntegerField(null=True, blank=True, verbose_name='Зарплата до')
    CURRENCY_OPTIONS = (
        ('RUR', 'руб.'),
        ('USD', 'USD'),
        ('EUR', 'EUR')
    )
    salary_currency = models.CharField(max_length=3, choices=CURRENCY_OPTIONS, verbose_name='Валюта',
                                       default='RUR', blank=True)

    company = models.ForeignKey('Employer', null=True, on_delete=models.CASCADE, verbose_name='Работодатель')
    city = models.ForeignKey('City', null=True, on_delete=models.SET_NULL, verbose_name='Город', blank=True)
    remote = models.BooleanField(default=False, verbose_name='Можно удаленно', blank=True)
    experience = models.CharField(max_length=100, blank=True, verbose_name='Требуемый опыт')

    EMPLOYMENT_STATUS = (
        ('f', 'Полная занятость'),
        ('p', 'Частичная занятость'),
        ('i', 'Стажировка'),
        ('p', 'Проектная работа'),
        ('v', 'Волонтерство'),
    )
    type_of_employment = models.CharField(max_length=1, choices=EMPLOYMENT_STATUS,
                                          verbose_name='Тип занятости', default=None)

    description = models.TextField(verbose_name='Описание')
    skills = models.ManyToManyField('Skill', null=True, blank=True, verbose_name='Навыки')
    published = models.DateTimeField(verbose_name='Дата публикации')
    hh_id = models.IntegerField(unique=True, verbose_name='HH ID')
    archived = models.BooleanField(default=False)
    page_views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def display_skills(self):
        return [skill.name for skill in self.skills.all()]

    def short_description(self):
        return self.description[:140] + '...'

    def display_salary(self):
        if self.salary_from and self.salary_up_to:
            return f'{intcomma(self.salary_from)}-{intcomma(self.salary_up_to)} {self.get_salary_currency_display()}'
        elif self.salary_from:
            return f'от {intcomma(self.salary_from)} {self.get_salary_currency_display()}'
        elif self.salary_up_to:
            return f'до {intcomma(self.salary_up_to)} {self.get_salary_currency_display()}'
        else:
            return 'З/п не указана'

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'


class City(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Город')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ['name']

class Employer(models.Model):
    name = models.CharField(max_length=300, unique=True, verbose_name='Работодатель')
    logo = models.URLField(max_length=500, null=True, verbose_name='Логотип', blank=True)
    description = models.TextField(null=True, verbose_name='Описание', blank=True)
    website = models.URLField(null=True, verbose_name='Сайт', blank=True)
    vacancies = models.ManyToManyField('Job', null=True, blank=True, verbose_name='Вакансии')

    page_views = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Работодатель'
        verbose_name_plural = 'Работодатели'

class Skill(models.Model):
    name = models.CharField(max_length=300, unique=True, verbose_name='Навык')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'