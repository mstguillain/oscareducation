# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.http import HttpResponse

from student_collaboration.models import StudentCollaborator, CollaborativeSettings
from .forms import StudentCollaboratorForm, CollaborativeSettingsForm


# Create your views here.
@login_required
def update_settings(request, collaborative_settings_pk=None):
    # requête de type POST; on update
    if collaborative_settings_pk:
        collaborative_settings = CollaborativeSettings.objects.get(pk=collaborative_settings_pk)
    else:
        collaborative_settings = CollaborativeSettings()

    # if student_collaborator_pk:
    #     student_collaborator = StudentCollaborator.objects.get(pk=student_collaborator_pk)
    # else:
    #     student_collaborator = StudentCollaborator()

    if request.method == 'POST':
        settings_set = CollaborativeSettingsForm(request.POST, instance=collaborative_settings)
        student_form = StudentCollaboratorForm(request.POST, instance=collaborative_settings)

        if student_form.is_valid() and settings_set.is_valid():
            settings_set.save()
            student_form.save()
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)
    else:
        collaborative_form = CollaborativeSettingsForm(instance=collaborative_settings)
        student_form = StudentCollaboratorForm(instance=collaborative_settings)
    return render(request, 'student_collaboration/student_settings.haml', {
        'student_form': student_form,
        'collaborative_form': collaborative_form
    })
