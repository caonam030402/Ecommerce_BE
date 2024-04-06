from django.db import models


from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    password = models.CharField(max_length=100)
    new_password = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    roles = models.ManyToManyField("Role")
    avatar = models.URLField(blank=True, null=True)


class Role(models.Model):
    name = models.CharField(max_length=50)
