from django.contrib import admin

# Register your models here.

from api.models.membership import Membership
admin.site.register(Membership)
