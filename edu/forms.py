from django import forms 
from .models import *

class TutorImageForm(forms.ModelForm): 
  
    class Meta: 
        model = Tutor 
        fields = ['image'] 