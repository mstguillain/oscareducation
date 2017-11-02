# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect

from student_collaboration.models import StudentCollaborator, CollaborativeSettings
from .forms import StudentCollaboratorForm, CollaborativeSettingsForm


# Create your views here.
@login_required
def update_settings(request):
    # requête de type POST; on update
    student = get_object_or_404(StudentCollaborator, pk=request.user.studentcollaborator.pk)
    settings = get_object_or_404(CollaborativeSettings, pk=request.user.studentcollaborator.settings.pk)

    if request.method == 'POST':
        settings_form = CollaborativeSettingsForm(request.POST, instance=settings)
        student_form = StudentCollaboratorForm(request.POST, instance=student)

        if student_form.is_valid() and settings_form.is_valid():
            settings = settings_form.save(commit=False)
            student = student_form.save(commit=False)
            student_form.settings = settings
            settings.save()
            student.save()
            return HttpResponseRedirect('/student_collaboration/settings/')

    # else:
    settings_form = CollaborativeSettingsForm(instance=settings)
    student_form = StudentCollaboratorForm(instance=student)
    return render(request, 'student_collaboration/student_settings.haml', {
        'student_form': student_form,
        'settings_form': settings_form
    })

def submit_help_request(request):
    return render(request, "student_collaboration/student_collaboration_home.haml")

def open_help_request(request):
    return render(request, "student_collaboration/student_collaboration_home.haml")

def collaborative_home(request):
    return render(request, 'student_collaboration/student_collaboration_home.haml')
