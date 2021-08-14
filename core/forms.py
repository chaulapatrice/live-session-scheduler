from django import forms
from .models import Expert
class AddExpertForm(forms.ModelForm):
    class Meta:
        model = Expert
        fields = ['name', 'email', 'description', 'contact']


class SelectExpertForm(forms.Form):
    expert_id = forms.IntegerField(widget=forms.HiddenInput())

class PickDatesForm(forms.Form):
    date_1 = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'datepicker'
    }))
    time_1 = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'timepicker'
    }))
    date_2 = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'datepicker'
    }))
    time_2 = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'timepicker'
    }))
    date_3 = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'datepicker'
    }))
    time_3 = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'timepicker'
    }))

class DateTimeConfirmationForm(forms.Form):
    date = forms.CharField(widget=forms.HiddenInput())
    time = forms.CharField(widget=forms.HiddenInput())