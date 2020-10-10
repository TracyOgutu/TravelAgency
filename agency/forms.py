from django import forms
from .models import Profile

class NewProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        exclude=['editor']
        widgets={
            'tags':forms.CheckboxSelectMultiple(),
        }