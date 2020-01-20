from django import forms
from .models import testFile, testScript


class uploadFileForms(forms.ModelForm):
    class Meta:
        model = testFile
        fields = ('zipFile',)


class runScriptForms(forms.Form):
    scriptId = forms.IntegerField(max_value=1000, widget=forms.HiddenInput)


class downloadReportForms(forms.Form):
    reportId = forms.IntegerField(max_value=1000, widget=forms.HiddenInput)


class deleteScriptForms(forms.Form):
    scriptId = forms.IntegerField(max_value=1000, widget=forms.HiddenInput)


class deleteReportForms(forms.Form):
    reportId = forms.IntegerField(max_value=1000, widget=forms.HiddenInput)
