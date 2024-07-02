from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Client(models.Model):
    client_name = models.CharField(max_length=255, default="Default Client Name")
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_clients')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='updated_clients')

class Project(models.Model):
    name = models.CharField(max_length=255)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='projects')
    users = models.ManyToManyField(User, related_name='assigned_projects')
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_projects', default=1)
