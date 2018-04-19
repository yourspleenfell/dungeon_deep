from django import forms
from .models import *

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ('name', 'image', )