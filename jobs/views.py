from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from django.views.generic import DetailView, ListView
from django.db.models import Count
from .models import Job, Employer,City
from .forms import JobFrom, EmployerForm, MainPageForm
from accounts.forms import UserRegistrationForm, UserLoginForm
from .utils import get_user_search_params, create_paginate_link


def jobs_list(request):
    context = dict()
    register_form = UserRegistrationForm
    login_form = UserLoginForm

    city = request.GET.get('city')
    type_of_employment = request.GET.getlist('type_of_employment')
    remote = request.GET.get('remote')
    search_field = request.GET.get('title')
    salary_from = request.GET.get('salary_from')
    skills = request.GET.getlist('skills')

    jobs = Job.objects.filter(archived=False)

    search_params = {}

    if type_of_employment:
        jobs = jobs.filter(type_of_employment__in=type_of_employment)
        search_params['type_of_employment'] = type_of_employment

    if city and not remote:
        jobs = jobs.filter(city=city)
        search_params['city'] = city
    if remote and not city:
        jobs = jobs.filter(remote=True)
        search_params['remote'] = remote
    if city and remote:
        jobs = jobs.filter(Q(city=city)|Q(remote=True))
        search_params['city'] = city
        search_params['remote'] = remote

    if search_field:
        jobs = jobs.filter(title__contains=search_field)
        search_params['search_field'] = search_field
    if skills:
        jobs = jobs.filter(skills__in=skills)
        search_params['skills'] = skills

    if salary_from == 'true':
        jobs = jobs.filter(Q(salary_from__isnull=False) | Q(salary_up_to__isnull=False))
        search_params['salary_from'] = salary_from
    elif salary_from:
        salary_rub_qs = Job.objects.filter(
                                Q(salary_from__gte=salary_from) |
                                Q(salary_up_to__gte=salary_from)
                                ).filter(salary_currency='RUR')

        salary_euro = int(salary_from)/90
        salary_usd = int(salary_from)/80

        salary_total_qs = salary_rub_qs.union(
            Job.objects.filter(Q(salary_from__gte=salary_euro) |
                               Q(salary_up_to__gte=salary_euro)
                               ).filter(salary_currency='EUR'),
            Job.objects.filter(Q(salary_from__gte=salary_usd) |
                               Q(salary_up_to__gte=salary_usd)
                               ).filter(salary_currency='USD')
        )

        jobs = jobs.intersection(salary_total_qs)
        search_params['salary_from'] = salary_from

    paginator = Paginator(jobs.distinct().order_by('-published'), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.user.is_authenticated:
        user_params = get_user_search_params(request)
        user_params_link = create_paginate_link(user_params)
        context['user_params_link'] = user_params_link


    form = JobFrom(initial=search_params)

    paginate_link = create_paginate_link(search_params)

    context.update({'jobs': page_obj, 'form': form, 'paginate_link' : paginate_link,
               'register_form' : register_form, 'login_form' : login_form})

    return render(request, 'jobs/job-listing.html', context)


class JobDetailView(DetailView):
    model = Job

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['register_form'] = UserRegistrationForm
        context['login_form'] = UserLoginForm
        if self.request.user.is_authenticated:
            user_params = get_user_search_params(self.request)
            user_params_link = create_paginate_link(user_params)
            context['user_params_link'] = user_params_link

        return context

    def get_object(self):
        obj = super().get_object()
        num_visits = self.request.session.get(f'job_{obj.id}_visits', 0)
        self.request.session[f'job_{obj.id}_visits'] = num_visits + 1
        if self.request.session[f'job_{obj.id}_visits'] == 1:
            obj.page_views += 1
            obj.save()
        return obj



class EmployerListView(ListView):
    model = Employer
    template_name = 'jobs/employer-listing.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = Employer.objects.filter(vacancies__isnull=False) \
                        .annotate(jobs_count=Count('vacancies')) \
                        .order_by('-jobs_count')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['register_form'] = UserRegistrationForm
        context['login_form'] = UserLoginForm

        search_field = self.request.GET.get('search')
        city = self.request.GET.get('city')
        remote = self.request.GET.get('remote')
        skills = self.request.GET.getlist('skills')

        search_params = {}

        queryset = self.get_queryset()

        if search_field:
            queryset = queryset.filter(Q(name__contains=search_field) |
                                       Q(name__contains=search_field.capitalize()) |
                                       Q(name__contains=search_field.upper())
                                       )
            search_params['search_field'] = search_field
        if city and not remote:
            queryset = queryset.filter(vacancies__city=city)
            search_params['city'] = city
        if remote and not city:
            queryset = queryset.filter(vacancies__remote=True)
            search_params['remote'] = remote
        if city and remote:
            queryset = queryset.filter(Q(vacancies__city=city) | Q(vacancies__remote=True))
            search_params['city'] = city
            search_params['remote'] = remote
        if skills:
            queryset = queryset.filter(vacancies__skills__in=skills)
            search_params['skills'] = skills

        paginator = Paginator(queryset, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['object_list'] = page_obj

        context['form'] = EmployerForm(initial=search_params)

        paginate_link = create_paginate_link(search_params)

        context['paginate_link'] = paginate_link

        if self.request.user.is_authenticated:
            user_params = get_user_search_params(self.request)
            user_params_link = create_paginate_link(user_params)
            context['user_params_link'] = user_params_link

        return context

class EmployerDetailView(DetailView):
    model = Employer
    #extra_context = {'register_form' : UserRegistrationForm, 'login_form' : UserLoginForm}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['register_form'] = UserRegistrationForm
        context['login_form'] = UserLoginForm
        if self.request.user.is_authenticated:
            user_params = get_user_search_params(self.request)
            user_params_link = create_paginate_link(user_params)
            context['user_params_link'] = user_params_link
        return context

    def get_object(self):
        obj = super().get_object()
        num_visits = self.request.session.get(f'emp_{obj.id}_visits', 0)
        self.request.session[f'emp_{obj.id}_visits'] = num_visits + 1
        self.request.session.modified = True
        if self.request.session[f'emp_{obj.id}_visits'] == 1:
            obj.page_views += 1
            obj.save()
        return obj

def index(request):
    context = dict()

    full_time_jobs = Job.objects.filter(archived=False, type_of_employment='f',
                                        remote=False).order_by('-published')[:4]

    remote_jobs = Job.objects.filter(archived=False, remote=True).order_by('-published')[:4]

    intern_jobs = Job.objects.filter(archived=False, type_of_employment='i',
                                        remote=False).order_by('-published')[:4]

    employers = Employer.objects.filter(vacancies__isnull=False, logo__isnull=False) \
                        .annotate(jobs_count=Count('vacancies')) \
                        .order_by('-jobs_count')
    register_form = UserRegistrationForm
    login_form = UserLoginForm
    job_form = MainPageForm

    jobs_total = Job.objects.filter(archived=False).count()
    employers_total = Employer.objects.filter(vacancies__isnull=False).distinct().count()
    cities = City.objects.all().count()

    if request.user.is_authenticated:
        user_params = get_user_search_params(request)
        user_params_link = create_paginate_link(user_params)
        context['user_params_link'] = user_params_link

    context.update({'full_time_jobs' : full_time_jobs, 'remote_jobs' : remote_jobs,
               'intern_jobs': intern_jobs, 'employers' : employers,
               'register_form' : register_form, 'login_form' : login_form,
               'jobs_total' : jobs_total, 'employers_total' : employers_total,
               'cities' : cities, 'job_form' : job_form})

    return render(request, 'jobs/index.html', context)