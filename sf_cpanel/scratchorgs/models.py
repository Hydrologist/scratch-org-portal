from django.db import models
from django.utils import timezone

class Organization(models.Model):
    access_token = models.CharField(max_length=200)
    access_url = models.URLField(max_length=250)
    alias = models.CharField(max_length=100, blank=True, default='')
    created_date = models.DateTimeField(auto_now_add=True)
    dev_hub = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
    )
    is_dev_hub = models.BooleanField(default=False)
    expiration_date = models.DateTimeField()
    expired_flag = models.BooleanField(default=False)
    instance_url = models.URLField(max_length=200)
    last_modified = models.DateTimeField(auto_now=True)
    login_url = models.URLField(max_length=100)
    organization_id = models.CharField(max_length=20)
    username = models.CharField(max_length=200, default='')

    @property
    def primary_user(self):
        users = self.salesforceuser_set.all()
        for user in users:
            if user.primary_user is True:
                return user
        return None

    @property
    def is_expired(self):
        return self.expired_flag is True or timezone.now() > self.expiration_date

    def __str__(self):
        return self.alias


class SalesforceUser(models.Model):
    username = models.CharField(max_length=200)
    profile_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    primary_user = models.BooleanField()
    created_date = models.DateTimeField(auto_now_add=True)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.username
