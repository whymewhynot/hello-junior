from django.contrib import admin
from .models import Job, Employer, Skill, City

admin.site.register(Employer)
admin.site.register(Skill)
admin.site.register(City)

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'city')



