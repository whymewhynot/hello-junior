from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from accounts.forms import UserLoginForm, UserRegistrationForm, UserProfileForm, MyPassChangeForm, MyPassResetForm
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from jobs.models import Job
from jobs.utils import get_user_search_params, create_paginate_link


class LoginOrRegisterView(View):
    def post(self, request):
        login_form = UserLoginForm(request.POST)
        register_form = UserRegistrationForm(request.POST)

        if login_form.is_valid():
            data = login_form.cleaned_data
            user = authenticate(request, username=data.get('email'),
                                password=data.get('password'))
            login(request, user)
            messages.success(request, f'Успешная авторизация {user}')
            # next_page = self.request.POST.get('next', 'index')
            # if next_page == 'login' or next_page == 'register':
            #     next_page = 'index'
            return redirect(self.request.POST.get('next', 'index'))

        if register_form.is_valid():
            data = register_form.cleaned_data
            new_user = register_form.save(commit=False)
            new_user.set_password(data['password'])
            new_user.save()
            messages.success(request, f'Успешная регистрация {new_user}')
            new_user = authenticate(request, username=data.get('email'),
                                    password=data.get('password'))
            login(request, new_user)
            return redirect(self.request.POST.get('next', 'profile'))

        return render(request, 'accounts/login-register.html', {'login_form': login_form,
                                              'register_form' : register_form})

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('profile')
        else:
            login_form = UserLoginForm(request.POST)
            register_form = UserRegistrationForm(request.POST)
            return render(request, 'accounts/login-register.html', {'login_form': login_form,
                                                  'register_form' : register_form})



def logout_view(request):
    logout(request)
    messages.success(request, 'Вы вышли из аккаунта')
    return redirect('login')


class UserProfileView(LoginRequiredMixin, View):
    login_url = 'login'
    def post(self, request):
        user = request.user
        form = UserProfileForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user.city = data['city']
            user.skills.clear()
            user.skills.set(data['skills'])
            user.is_subscribed = data['is_subscribed']
            user.remote = data['remote']
            user.save()
            messages.success(request, 'Данные обновлены')
            return redirect('profile')

        data = self.get_initital_data(request)
        form = UserProfileForm(initial=data)

        user_params = get_user_search_params(self.request)
        user_params_link = create_paginate_link(user_params)

        return render(request, 'accounts/profile.html', {'form': form, 'user_params_link' : user_params_link})

    def get(self, request):
        data = self.get_initital_data(request)
        form = UserProfileForm(initial=data)

        user_params = get_user_search_params(self.request)
        user_params_link = create_paginate_link(user_params)

        return render(request, 'accounts/profile.html', {'form' : form, 'user_params_link' : user_params_link})

    def get_initital_data(self, request):
        user = request.user
        data = {'city': user.city,
                'is_subscribed': user.is_subscribed,
                'skills': user.skills.all(),
                'remote' : user.remote}
        return data

class MyPasswordChangeView(PasswordChangeView):
    template_name='accounts/password_change_form.html'
    success_url = reverse_lazy('profile')
    form_class = MyPassChangeForm

    def form_valid(self, form):
        messages.success(self.request, 'Пароль успешно изменён')
        return super().form_valid(form)

class MyPasswordResetView(PasswordResetView):
    template_name='accounts/password_reset_form.html'
    success_url = reverse_lazy('password_reset')

    def form_valid(self, form):
        messages.success(self.request, 'Ссылка на сброс пароля отправлена')
        return super().form_valid(form)

class MyPassResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('profile')
    form_class = MyPassResetForm

    def form_valid(self, form):
        messages.success(self.request, 'Пароль успешно изменён, можете использовать его для входа')
        return super().form_valid(form)


@login_required
def add_or_remove_favorite(request, id):
    if request.method == 'POST':
        user = request.user
        job = Job.objects.filter(id=id).get()

        if job in user.favorites.all():
            user.favorites.remove(id)
            messages.success(request, 'Вакансия удалена из избранного')
        else:
            user.favorites.add(id)
            messages.success(request, 'Вакансия добавлена в избранное')

    return redirect(request.POST.get('url_from'))

@login_required
def favorites_view(request):
    context = dict()
    jobs = request.user.favorites.all()
    context['jobs'] = jobs

    if request.user.is_authenticated:
        user_params = get_user_search_params(request)
        user_params_link = create_paginate_link(user_params)
        context['user_params_link'] = user_params_link

    return render(request, 'accounts/favorites.html', context)