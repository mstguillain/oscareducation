from django import forms

from .models import StudentCollaborator, CollaborativeSettings, HelpRequest


class StudentCollaboratorForm(forms.ModelForm):
    class Meta:
        model = StudentCollaborator
        fields = ['code_postal', 'collaborative_tool', 'settings']

class CollaborativeSettingsForm(forms.ModelForm):
    class Meta:
        model = CollaborativeSettings
        fields = ['distance']