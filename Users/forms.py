from django import forms
from django.contrib.auth.models import User

class signInForm(forms.Form):
    username = forms.CharField(max_length=20, widget=forms.TextInput)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)


class signUpForm(forms.ModelForm):
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)
    passwordConfirm = forms.CharField(max_length=20, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_passwordConfirm(self):
        cd = self.cleaned_data
        if cd['password'] != cd['passwordConfirm']:
            raise forms.ValidationError(r"The two password fields didn't match.")
        return cd['passwordConfirm']
