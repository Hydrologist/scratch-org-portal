from django import forms

class CreateOrgForm(forms.Form):
    alias = forms.CharField(max_length=100)