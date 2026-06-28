from django.contrib import admin
from cases.models import *
# Register your models here.

admin.site.register(Case)
admin.site.register(Lawyer)
admin.site.register(Client)

# change in the dashboard
# class CaseAdmin(admin.ModelAdmin):
#     list_display = ('case_number', 'title', 'status', 'client', 'lawyer', 'created_at')
#     search_fields = ('case_number', 'title')

# admin.site.register(Case, CaseAdmin)
# Add to admin.py
from .models import Hearing

admin.site.register(Hearing)