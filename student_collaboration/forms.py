from django import forms

from .models import StudentCollaborator, CollaborativeSettings, HelpRequest


class StudentCollaboratorFormCollaborativeTool(forms.ModelForm):
    class Meta:
        model = StudentCollaborator
        fields = ['collaborative_tool']

class StudentCollaboratorFormPostalCode(forms.ModelForm):
    class Meta:
        model = StudentCollaborator
        fields = ['postal_code']

class CollaborativeSettingsForm(forms.ModelForm):
    class Meta:
        model = CollaborativeSettings
        fields = ['distance']


class UnmasteredSkillsForm(forms.Form):
    def __init__(self, qs=None, *args, **kwargs):
        super(UnmasteredSkillsForm, self).__init__(*args, **kwargs)
        self.fields['liste'] = forms.ModelMultipleChoiceField(queryset=qs)

class HelpRequestForm(forms.Form):
     def __init__(self, *args, **kwargs):
         helprequest = kwargs.pop('HelpRequests')
         super(HelpRequestForm, self).__init__(*args, **kwargs)
         for q in helprequest:
             self.fields['HelpRequests'] = forms.CharField(label=HelpRequest.skill)

