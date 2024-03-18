from django.forms import ModelForm
from .models import Group, Messages
from django.contrib.auth.models import User

class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = '__all__'
        exclude = ['admin']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']