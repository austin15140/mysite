from django import forms
from django.forms.widgets import Textarea
from users.models import UserProfile, get_randfile_path, UserFile
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    description = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'cols': 80, 'rows': 5}))
    class Meta:
        model = UserProfile
        exclude = {'user', 'description'}

class NewUser(forms.Form):
    username = forms.CharField(max_length=50)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)

class FileForm(forms.ModelForm):
    class Meta:
        model = UserFile

class Del_Video(forms.Form):
    Delete = forms.BooleanField()

class Del_File(forms.Form):
    Delete = forms.BooleanField()

class Del_Photo(forms.Form):
    Delete = forms.BooleanField()