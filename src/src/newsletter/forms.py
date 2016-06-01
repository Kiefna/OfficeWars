from django import forms
from .models import SignUp
from .models import War
from django.contrib.auth.models import User
from datetimewidget.widgets import DateTimeWidget
from ajax_select.fields import AutoCompleteField, AutoCompleteSelectMultipleField
from ajax_select import make_ajax_field


class ContactForm(forms.Form):
    full_name = forms.CharField(required=False)
    email = forms.EmailField()
    message = forms.CharField()


class PlayerForm(forms.Form):
    player_name = forms.CharField(required=False)


class WarForm(forms.ModelForm):
    class Meta:
        model = War
        # fields = ['war_name', 'war_type', 'status', 'value', 'date_time_start']  # 'players'
        widgets = {
            'datetime': DateTimeWidget(attrs={'id': "yourdatetimeid"}, usel10n=True, bootstrap_version=3)
        }
        fields = ['war_name', 'war_type', 'value', 'datetime', "description"]  # 'status'


class PlayerSearch(forms.ModelForm):
    username = AutoCompleteField('username', show_help_text=False)

    class Meta:
        fields = ['username']
        model = User


class SignUpForm(forms.ModelForm):
    class Meta:
        model = SignUp
        fields = ['full_name', 'email']
    # exclude = ['full_name']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_base, provider = email.split("@")
        domain, extension = provider.split('.')
        # if not domain == 'USC':
        # 	raise forms.ValidationError("Please make sure you use your USC email.")
        if not extension == "edu":
            raise forms.ValidationError("Please use a valid .EDU email address")
        return email

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        # write validation code.
        return full_name

