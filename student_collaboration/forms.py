from django import forms

from .models import StudentCollaborator, CollaborativeSettings


class StudentCollaboratorForm(forms.ModelForm):
    class Meta:
        model = StudentCollaborator
        fields = ['code_postal', 'collaborative_tool']


class CollaborativeSettingsForm(forms.ModelForm):
    class Meta:
        model = CollaborativeSettings
        fields = ['distance']
