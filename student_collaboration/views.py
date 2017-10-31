# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from .forms import StudentCollaboratorForm


# Create your views here.
@login_required
def update_settings(request):
    # requête de type POST; on update
    if request.method == 'POST':
        student_form = StudentCollaboratorForm(request.POST, instance=request.user.collaborative_tool)
        if student_form.is_valid():
            student_form.save()
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)
    else:
        student_form = StudentCollaboratorForm(instance=request.user.collaborative_tool)
    return render(request, 'student_collaboration/student_settings.haml', {
        'student_form': student_form
    })
