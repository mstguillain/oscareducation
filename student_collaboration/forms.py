from django import forms
from django.forms import IntegerField, NumberInput

from .models import StudentCollaborator, CollaborativeSettings, HelpRequest


class StudentCollaboratorForm(forms.ModelForm):
    class Meta:
        model = StudentCollaborator
        fields = ['postal_code', 'collaborative_tool']


class CollaborativeSettingsForm(forms.ModelForm):
    class Meta:
        model = CollaborativeSettings
        fields = ['distance']
        widgets = {
            'distance': NumberInput(attrs={'min':0,'max': '100'})
        }


class UnmasteredSkillsForm(forms.Form):

    def __init__(self, *args, **kwargs):
        qs = kwargs.pop('skills', None)
        self.current_user = kwargs.pop('current_user', None)
        super(UnmasteredSkillsForm, self).__init__(*args, **kwargs)
        self.fields['list'] = forms.ModelMultipleChoiceField(queryset=qs, label="")

    # custom method to do validation
    # https://docs.djangoproject.com/fr/1.11/ref/forms/validation/#cleaning-a-specific-field-attribute
    def clean_list(self):
        skills = self.cleaned_data['list']

        # checks if the current user has exceed its MAX help request limit
        count = HelpRequest.objects\
            .filter(student__pk=self.current_user, skill=skills)\
            .exclude(state=HelpRequest.CLOSED)\
            .count()

        if count >= HelpRequest.MAX_HELP_REQUEST_BY_SKILLS:
            raise forms.ValidationError("Vous avez atteint la limite. Veuilez cloturer des demandes")

        return skills


class HelpRequestForm(forms.Form):
    def __init__(self, *args, **kwargs):
        helprequest = kwargs.pop('HelpRequests')
        super(HelpRequestForm, self).__init__(*args, **kwargs)
        for q in helprequest:
            self.fields['HelpRequests'] = forms.CharField(label=HelpRequest.skill)
