from django import forms
from .models import SignUp
from .models import War, Profile, Office
from django.contrib.auth.models import User
from datetimewidget.widgets import DateTimeWidget
from ajax_select.fields import AutoCompleteField, AutoCompleteSelectMultipleField
from ajax_select import make_ajax_field
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field
from foundation_filefield_widget.widgets import FoundationFileInput, FoundationImageInput


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

        # def clean_war_name(self):
        #     # cleaned_data = super(WarForm, self).clean()
        #     war_name = self.cleaned_data.get('war_name')
        #     checkwarname = War.objects.filter(war_name=war_name)
        #     war_name = war_name.replace(" ", "-")
        #     if checkwarname[0]:
        #         raise forms.ValidationError("That War Name is already in use. Please use a Different War Name")
        #     else:
        #         return war_name


class PlayerSearch(forms.ModelForm):
    username = AutoCompleteField('username', show_help_text=False)

    def __init__(self, *args, **kwargs):
        # instance = kwargs.get('instance', None)
        #
        # kwargs.update(initial={
        #     # 'field': 'value'
        #     'title': '1020',
        #     'description': 'huh'
        # })

        super(PlayerSearch, self).__init__(*args, **kwargs)
        # self.fields['profilePicture'].initial = self.request.user.Profile

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False

    class Meta:
        fields = ['username']
        model = User


class OfficeSearch(forms.ModelForm):
    officeName = AutoCompleteField('office', show_help_text=False, required=False)

    class Meta:
        fields = ['officeName']
        model = Office


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


class UserProfileUpdateForm1(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # instance = kwargs.get('instance', None)
        #
        # kwargs.update(initial={
        #     # 'field': 'value'
        #     'title': '1020',
        #     'description': 'huh'
        # })

        super(UserProfileUpdateForm1, self).__init__(*args, **kwargs)
        # self.fields['profilePicture'].initial = self.request.user.Profile

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False

    class Meta:
        model = User
        fields = ['email']


class UserProfileUpdateForm2(forms.ModelForm):
    # def get_form_kwargs(self):
    #     kwargs = super(UserProfileUpdateForm2, self).get_form_kwargs()
    #     kwargs['initial'] = {
    #         "title":
    #     }  # your initial data here
    #     return kwargs
    def __init__(self, *args, **kwargs):
        # """If no initial data, provide some defaults."""
        # initial = kwargs.get('initial', {})
        # initial['title'] = 'Test'
        # initial['description'] = 'Test2'
        # kwargs['initial'] = initial
        super(UserProfileUpdateForm2, self).__init__(*args, **kwargs)

        # def __init__(self, *args, **kwargs):
        # instance = kwargs.get('instance', None)
        #
        # kwargs.update(initial={
        #     # 'field': 'value'
        #     'title': '1020',
        #     'description': 'huh'
        # })
        # title = kwargs.pop('title', None)
        # description = kwargs.pop('description', None)
        #
        # print "_-_-_-_-"
        # print title
        # print description
        # print "_-_-_-_-"
        # self.fields['title'].initial = title
        # # print self.fields['title'].initial
        # # print self.fields['description'].initial
        # self.fields['description'].initial = description
        # initial_fields = ["title", "description"]
        #
        # initial = kwargs.pop('initial', {})
        # initial["title"] = initial.get("title") or getattr(self.person, "title")
        # kwargs['initial'] = initial

        # super(UserProfileUpdateForm2, self).__init__(*args, **kwargs)
        # self.fields['profilePicture'].initial = self.request.user.Profile
        # print "2_-_-_-_-2"
        # print self.fields['title'].initial
        # self.initial['title'] = title
        # # print self.fields['title'].initial
        # # print self.fields['description'].initial
        # self.initial['description'] = description
        # print "****"
        # print self.initial['description']
        # print "****"
        # print self.fields['description'].initial
        # print "2_-_-_-_-2"
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        # self.helper = FormHelper(self)
        # self.helper.form_tag = False
        # self.helper.layout = Layout(
        #     Field('profilePicture'),
        # )

        # self.helper.form_tag = False

        # self.helper.layout = Layout(
        #     Fieldset(
        #         'Profile Picture'
        #     ),
        #
        #     ButtonHolder(
        #         Submit('update', 'Update', css_class='btn btn-default')
        #     )
        # )

        # You can dynamically adjust your layout
        # self.helper.layout.append(Submit('save', 'save'))

    class Meta:
        model = Profile
        fields = ['title', 'description']
        # fields = ['profilePicture']


class UserProfileUpdateForm3(forms.ModelForm):
    # def get_form_kwargs(self):
    #     kwargs = super(UserProfileUpdateForm2, self).get_form_kwargs()
    #     kwargs['initial'] = {
    #         "title":
    #     }  # your initial data here
    #     return kwargs
    def __init__(self, *args, **kwargs):
        """If no initial data, provide some defaults."""
        # initial = kwargs.get('initial', {})
        # initial['title'] = 'Test'
        # initial['description'] = 'Test2'
        # kwargs['initial'] = initial
        super(UserProfileUpdateForm3, self).__init__(*args, **kwargs)

        # def __init__(self, *args, **kwargs):
        # instance = kwargs.get('instance', None)
        #
        # kwargs.update(initial={
        #     # 'field': 'value'
        #     'title': '1020',
        #     'description': 'huh'
        # })
        # title = kwargs.pop('title', None)
        # description = kwargs.pop('description', None)
        #
        # print "_-_-_-_-"
        # print title
        # print description
        # print "_-_-_-_-"
        # self.fields['title'].initial = title
        # # print self.fields['title'].initial
        # # print self.fields['description'].initial
        # self.fields['description'].initial = description
        # initial_fields = ["title", "description"]
        #
        # initial = kwargs.pop('initial', {})
        # initial["title"] = initial.get("title") or getattr(self.person, "title")
        # kwargs['initial'] = initial

        # super(UserProfileUpdateForm2, self).__init__(*args, **kwargs)
        # self.fields['profilePicture'].initial = self.request.user.Profile
        # print "2_-_-_-_-2"
        # print self.fields['title'].initial
        # self.initial['title'] = title
        # # print self.fields['title'].initial
        # # print self.fields['description'].initial
        # self.initial['description'] = description
        # print "****"
        # print self.initial['description']
        # print "****"
        # print self.fields['description'].initial
        # print "2_-_-_-_-2"
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        # self.helper = FormHelper(self)
        # self.helper.form_tag = False
        # self.helper.layout = Layout(
        #     Field('profilePicture'),
        # )

        # self.helper.form_tag = False

        # self.helper.layout = Layout(
        #     Fieldset(
        #         'Profile Picture'
        #     ),
        #
        #     ButtonHolder(
        #         Submit('update', 'Update', css_class='btn btn-default')
        #     )
        # )

        # You can dynamically adjust your layout
        # self.helper.layout.append(Submit('save', 'save'))

    class Meta:
        model = Profile
        fields = ['profilePicture']
        # fields = ['profilePicture']


class OfficeCreate(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # instance = kwargs.get('instance', None)
        #
        # kwargs.update(initial={
        #     # 'field': 'value'
        #     'title': '1020',
        #     'description': 'huh'
        # })

        super(OfficeCreate, self).__init__(*args, **kwargs)
        # self.fields['profilePicture'].initial = self.request.user.Profile

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_tag = False

    class Meta:
        model = Office
        fields = ['officeName', 'officeSize', 'officeType', 'officeDescription', 'officeShield']


class ChatForm(forms.Form):
    message = forms.CharField(required=False, max_length=200, label="")
