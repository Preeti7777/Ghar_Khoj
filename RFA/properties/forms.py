from django.forms import ModelForm

from django import forms
from .models import Facility, Property


class PropertyForm(ModelForm):
    lalpurja_image = forms.ImageField(required=True)
    rules = forms.CharField(required=True, widget=forms.Textarea)

    class Meta:
        model = Property
        exclude = ['owner', 'status', 'created_at']


class FacilityForm(ModelForm):
    class Meta:
        model = Facility
        exclude = ['property']
