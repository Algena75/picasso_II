from django.contrib import admin

from bicycles.models import Bicycle, Rent
from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'rented',
    )
    list_editable = ('username',)
    list_filter = ('rented',)


class BicycleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'number',
        'is_rented',
    )
    list_editable = ('number',)
    list_filter = ('is_rented',)


class RentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'bicycle',
        'renter',
        'start_time',
        'finish_time',
        'value'
    )


admin.site.register(Bicycle, BicycleAdmin)
admin.site.register(Rent, RentAdmin)
admin.site.register(User, UserAdmin)
