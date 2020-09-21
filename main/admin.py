from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Event

class MyUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'mobile_number', 'email']
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('mobile_number', 'address','pancard','coins')}),
    )

admin.site.register(User, MyUserAdmin)
admin.site.register(Event)
