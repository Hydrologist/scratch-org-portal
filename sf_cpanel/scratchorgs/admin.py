from django.contrib import admin

# Register your models here.
from .models import Organization, SalesforceUser

admin.site.register(Organization)
admin.site.register(SalesforceUser)
