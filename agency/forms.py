from django import forms
from .models import Profile,Reviews

class NewProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        exclude=['editor']
        widgets={
            'tags':forms.CheckboxSelectMultiple(),
        }

class NewReviewForm(forms.ModelForm):
    class Meta:
        model=Reviews
        exclude=['reviewer','review_date',]
        widgets={
            'tags':forms.CheckboxSelectMultiple(),
        }

