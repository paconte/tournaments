from django import forms
from django.core.exceptions import ValidationError

from player.models import Contact
from player.models import Team
from player.models import Person
from player.models import Tournament


class SearchForm(forms.Form):
    text = forms.CharField(label='Search', required=True, max_length=40,
            widget=forms.TextInput(attrs={'class': 'form-control',
                                          'placeholder': 'Enter a player, team or tournament name'}))


class PersonSearchForm(forms.ModelForm):
    first_name = forms.CharField(label='First name',
                                 required=False,
                                 max_length=40,
                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'placeholder': 'Enter first name'}))
    last_name = forms.CharField(label='Last name',
                                required=False,
                                max_length=40,
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': 'Enter last name'}))

    class Meta:
        model = Person
        fields = ['first_name', 'last_name']


class TeamSearchForm(forms.ModelForm):
    name = forms.CharField(label='Team name',
                           required=True,
                           max_length=40,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'Enter name',
                                                         'required': 'True'}))

    class Meta:
        model = Team
        fields = ['name']


class TournamentSearchForm(forms.ModelForm):
    name = forms.CharField(label='Tournament name',
                           required=True,
                           max_length=40,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'Enter name',
                                                         'required': 'True'}))

    class Meta:
        model = Tournament
        fields = ['name']


class ContactForm(forms.ModelForm):
    name = forms.CharField(label='Your name',
                           required=True,
                           max_length=40,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'Enter name',
                                                         'required': 'True'}))
    email = forms.EmailField(label='Your email',
                             required=True,
                             max_length=50,
                             widget=forms.TextInput(attrs={'class': 'form-control',
                                                           'placeholder': 'Enter email',
                                                           'required': 'True'}))
    confirm_email = forms.EmailField(label='Confirm email',
                                     required=True,
                                     max_length=50,
                                     widget=forms.TextInput(attrs={'class': 'form-control',
                                                                   'placeholder': 'Enter email',
                                                                   'required': 'True'}))
    where = forms.CharField(label='Where do you play touch?',
                            required=False,
                            max_length=20,
                            widget=forms.TextInput(attrs={'class': 'form-control',
                                                          'placeholder': 'Enter your city and/or country'}))
    message = forms.CharField(label='Message',
                              required=True,
                              min_length=10,
                              widget=forms.Textarea(attrs={'class': 'form-control',
                                                           'required': 'True'}))
    spamchecker = forms.CharField(label='What is 4+3?',
                                  required=True,
                                  max_length=5,
                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'placeholder': 'Enter sum',
                                                                'required': 'True'}))

    class Meta:
        model = Contact
        fields = ['name', 'email', 'where', 'message']

    def clean(self):
        #        form_data = super(ContactForm, self).clean()
        print(form_data)
        #        if form_data.get('email') is None:
        #            self._errors['email'] = ['Email is not valid.']
        #            raise forms.ValidationError("Email field is empty.")
        #        if form_data.get('confirm_email') is None:
        #            self._errors['confirm_email'] = ['Email is not valid.']
        #            raise forms.ValidationError("Email field is empty.")
        if form_data.get('email') != form_data.get('confirm_email'):
            self._errors['confirm_email'] = ['Email confirmation does not match.']
            raise forms.ValidationError("Email confirmation does not match.")
        if form_data.get('spamchecker') is None or form_data.get('spamchecker') != '7':
            self._errors['spamchecker'] = ['Wrong value.']
            raise forms.ValidationError("Wrong value.")
        return self.cleaned_data

    def clean_name(self):
        name = self.cleaned_data['name']
        if name is None:
            self._errors['name'] = ['Name is empty.']
            raise form.ValidationError("Name field is empty.")
        return name

    def clean_message(self):
        message = self.cleaned_data['message']
        if message is None:
            self._errors['message'] = ['Message is empty.']
            raise ValidationError("Message field is empty.")
        return message

    def clean_spamchecker(self):
        spamchecker = self.cleaned_data['spamchecker']
        print('clean_spam_checker()')
        return spamchecker
