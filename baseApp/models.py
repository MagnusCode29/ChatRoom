from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Cluster(models.Model):
    clusterName = models.CharField(max_length = 200)

    def __str__(self):
        return self.clusterName
class Group(models.Model):
    admin = models.ForeignKey(User, null = True, on_delete = models.SET_NULL)
    cluster = models.ForeignKey(Cluster, on_delete = models.SET_NULL, null = True)
    GroupName = models.CharField(max_length = 200)
    GroupDescription = models.TextField(null = True, blank = True)
    updatedTime = models.DateTimeField(auto_now = True)
    createdTime = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['-createdTime']

    def __str__(self):
        return self.GroupName

class Messages(models.Model):
    group = models.ForeignKey(Group, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    content = models.TextField()
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.content[0:40]