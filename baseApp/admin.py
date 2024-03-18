from django.contrib import admin
from .models import Group, Cluster, Messages
# Register your models here.

admin.site.register(Group)
admin.site.register(Cluster)
admin.site.register(Messages)