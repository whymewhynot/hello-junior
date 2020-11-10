from django import forms
from jobs.models import Job, Skill,City

top_skills = ['Java', 'C', 'Python', 'C++', 'C#', 'JavaScript', 'PHP', 'Objective-C',
                  'R', 'Swift', 'TypeScript', 'Ruby', 'HTML', 'CSS', 'Scala',
                  'Go', 'Kotlin', 'Matlab', 'Ruby On Rails']

salary_choices = [
                ('true', 'Указана'),
                ('30000', 'от 30 000 руб.'),
                ('60000', 'от 60 000 руб.'),
                ('120000', 'от 120 000 руб.')
                 ]


class JobFrom(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['skills'].queryset = Skill.objects.filter(name__in=top_skills)

    class Meta:
        model = Job
        labels = ''
        fields = ['type_of_employment', 'city', 'remote', 'title', 'salary_from', 'skills']

        widgets = {
            'type_of_employment' : forms.CheckboxSelectMultiple(),
            'city' : forms.Select(attrs={'class': 'nice-select wide', 'style' : 'display: none;'}),
            'remote' : forms.CheckboxInput(),
            'title' : forms.TextInput(attrs={'placeholder' : 'Поиск по названию...', 'class': 'w-100'}),
            'salary_from' : forms.RadioSelect(choices=salary_choices),
            'skills' : forms.CheckboxSelectMultiple()
                    }

class EmployerForm(forms.Form):
    search = forms.CharField(required=False,
                             widget=forms.TextInput(attrs={'placeholder' : 'Название компании...',
                                                           'class': 'w-100'})
                             )
    city = forms.ModelChoiceField(queryset=City.objects.all(),
                                  widget=forms.Select(attrs={'class': 'nice-select wide'}),
                                  required=False
                                  )

    remote = forms.BooleanField(required=False)
    
    skills = forms.ModelChoiceField(required=False,
                                    queryset=Skill.objects.filter(name__in=top_skills),
                                    widget=forms.CheckboxSelectMultiple(),
                                    empty_label=None)

class MainPageForm(JobFrom):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].empty_label = 'Город'
        self.fields['title'].widget.attrs['placeholder'] = 'Какую работу вы ищете?'
        self.fields['salary_from'].widget = forms.Select(attrs={'class': 'nice-select wide'})
        self.fields['salary_from'].widget.choices = [(None, 'Зарплата')] + salary_choices