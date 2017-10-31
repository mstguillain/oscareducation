from django import forms

from .models import StudentCollaborator, CollaborativeSettings, HelpRequest


class StudentCollaboratorForm(forms.ModelForm):
    class Meta:
        model = StudentCollaborator


class CollaborativeSettingsForm(forms.ModelForm):
    class Meta:
        model = CollaborativeSettings
