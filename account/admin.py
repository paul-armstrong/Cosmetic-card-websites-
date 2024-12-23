from django.contrib import admin
from .models import Account
# from  django.contrib.auth.admin import UserAdmin
# Register your models here.

class Account_admin(admin.ModelAdmin):
    list_display=('email','first_name','last_name','last_login','is_active','is_superadmin')
    ordering=('-date_joined',)
    readonly_fields=('last_login','date_joined')
    filter_horizontal=()
    list_filter=()
    fieldsets=()
    list_display_links=('email','first_name','last_name','last_login','is_active','is_superadmin')
admin.site.register(Account,Account_admin)