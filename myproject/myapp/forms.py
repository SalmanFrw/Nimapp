from django import forms
from .models import Client, Project, User

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
