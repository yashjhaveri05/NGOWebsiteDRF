from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Event,Donation,Redeem

class MyUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'mobile_number', 'email']
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('mobile_number', 'address','pancard','coins')}),
    )

class EventAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Title", {'fields': ["title"]}),
        ("Volunteers", {'fields': ["volunteers"]}),
        ("Description", {'fields': ["description"]}),
        ("Cause", {'fields': ["cause"]}),
        ("Location", {'fields': ["location"]}),
        ("Duration", {'fields': ["duration"]}),
        ("Event Timings", {'fields': ["event_timings"]}),
        ("Created By", {'fields': ["created_by"]}),
        ("Completed", {'fields': ["is_complete"]}),
    ]
    list_display = ('title','location','cause','event_timings','is_complete')

class DonationAdmin(admin.ModelAdmin):
    list_display = ('donated_by','amount_donated','donated_on', 'bank_name', 'bank_branch', 'payment_method')

admin.site.register(User, MyUserAdmin)
admin.site.register(Event)
admin.site.register(Donation,DonationAdmin)
admin.site.register(Redeem)