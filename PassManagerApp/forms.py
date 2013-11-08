# -*- coding: utf-8 -*-
import re
from django.contrib.auth.models import User
from django import forms
#The forms to be used to the app
#Starting with the registration form
class RegistrationForm(forms.Form):
    username = forms.CharField(label=u'Username', max_length=30)
    first_name = forms.CharField(label=u'First Name', max_length=30)
    last_name = forms.CharField(label=u'Last Name', max_length=30)
    email = forms.EmailField(label=u'Email')
    password1 = forms.CharField(
                                label=u'Password',
                                widget=forms.PasswordInput()
                                )
    password2 = forms.CharField(
                                label=u'Password (Again)',
                                widget=forms.PasswordInput()
                                )
    #validation if pass1=pass2, if user exists and english characters
    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
        if password1 == password2:
            return password2

        raise forms.ValidationError('Passwords do not match.')
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not re.search(r'^\w+$', first_name):
            raise forms.ValidationError('First Name can only contain '
                                        'alphanumeric (English) characters and the underscore.')
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not re.search(r'^\w+$', last_name):
            raise forms.ValidationError('Last Name can only contain '
                                        'alphanumeric (English) characters and the underscore.')
        return last_name

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('Username can only contain '
                                    'alphanumeric (English) characters and the underscore.')
        try:
                User.objects.get(username=username)
        except User.DoesNotExist:
                    return username
        raise forms.ValidationError('Username is already taken.')
#the form to be used for saving logins
class LoginSaveForm(forms.Form):
    name = forms.CharField(
                         label=u'Site Name',
                         widget=forms.TextInput(attrs={'size': 64})
                         )
    url = forms.URLField(
                          label=u'Url',
                          widget=forms.TextInput(attrs={'size': 64})
                          )
    Login_username = forms.CharField(
                          label=u'Username',
                          widget=forms.TextInput(attrs={'size': 64})
                          )
    password = forms.CharField(
                          widget=forms.PasswordInput,
                          label=u'Password'
                              )
    notes = forms.CharField(
                          label=u'Notes',
                          widget=forms.Textarea(attrs={'size': 64,'cols': 46, 'rows': 5})
                          )
#the form to be used for editing logins
class LoginEditForm(forms.Form):
    name = forms.CharField(
                           label=u'Site Name',
                           widget=forms.TextInput(attrs={'size': 64})
                           )
    url = forms.URLField(
                         label=u'Url',
                         widget=forms.TextInput(attrs={'size': 64})
                         )
    Login_username = forms.CharField(
                                     label=u'Username',
                                     widget=forms.TextInput(attrs={'size': 64})
                                     )
    password = forms.CharField(
                               widget=forms.TextInput,
                               label=u'Password'
                               )
    notes = forms.CharField(
                            label=u'Notes',
                            widget=forms.Textarea(attrs={'size': 64,'cols': 46, 'rows': 5})
                            )
    id = forms.CharField(
                            widget=forms.HiddenInput()
                            )