# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.views.generic import ListView

from student_collaboration.models import StudentCollaborator, CollaborativeSettings, HelpRequest
from users.models import Student
from skills.models import Skill
from .forms import StudentCollaboratorForm, CollaborativeSettingsForm, UnmasteredSkillsForm, HelpRequestForm
from math import sin, cos, sqrt, atan2, radians


# Create your views here.
@login_required
def update_settings(request):
    # requête de type POST; on update
    true_student = get_object_or_404(Student, user=request.user.pk)
    student = get_object_or_404(StudentCollaborator, pk=true_student.studentcollaborator.pk)
    settings = get_object_or_404(CollaborativeSettings, pk=true_student.studentcollaborator.settings.pk)

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

@login_required
def submit_help_request(request):
    student_collab = get_object_or_404(StudentCollaborator, pk=request.user.student.studentcollaborator.pk)
    list_skills_id = student_collab.get_unmastered_skills()
    if list_skills_id:
        list_skill_unmastered = Skill.objects.filter(id__in=list_skills_id)
    else:
        list_skill_unmastered = list_skills_id #student had no skill, no need to filter => empty query set

    if request.method == 'POST':
        form = UnmasteredSkillsForm(list_skill_unmastered, request.POST)
        if form.is_valid(): # All validation rules pass
            form.liste = form.cleaned_data['liste']
            settings = get_object_or_404(CollaborativeSettings, pk=request.user.student.studentcollaborator.settings.pk)
            created_hr = student_collab.launch_help_request(settings)
            for skill in form.cleaned_data.get("liste"):
                created_hr.skill.add(skill)
            return HttpResponseRedirect("/student_collaboration/")
    else:
        skill_form = UnmasteredSkillsForm(list_skill_unmastered)

    return render(request, "student_collaboration/request_help.haml", {
        'skill_form': skill_form
    })


@login_required
def open_help_request(request, id=None):
    if id:
        hp = HelpRequest.objects.filter(id=id).first()
        hp.reply_to_unanswered_help_request(request.user.student)

    """ On redirige vers la list view """
    return redirect('provide_help')


def collaborative_home(request):
    return render(request, 'student_collaboration/student_collaboration_home.haml')


class OpenHelpRequestsListView(ListView):
    model = HelpRequest
    paginate_by = 10
    template_name = "student_collaboration/open_help_requests_list.haml"
    context_object_name = "open_help_requests"

    def get_queryset(self):
        open_help_requests = HelpRequest.objects.filter(state=HelpRequest.OPEN)
        filtered_help_requests = []
        # on ne prend que ceux dans notre area
        for help_request in open_help_requests:
            """ Formule de Haversine pour connaitre la distance entre deux points géographiques """
            earth_radius = 6373.0

            lat1 = radians(help_request.student.studentcollaborator.postal_code.latitude)
            lon1 = radians(help_request.student.studentcollaborator.postal_code.longitude)
            lat2 = radians(self.request.user.student.studentcollaborator.postal_code.latitude)
            lon2 = radians(self.request.user.student.studentcollaborator.postal_code.longitude)

            dlon = lon2 - lon1
            dlat = lat2 - lat1

            a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))

            distance = earth_radius * c
            if distance <= help_request.settings.distance:
                filtered_help_requests.append(help_request)

        """ On peut toujours filtrer """
        """ https://stackoverflow.com/a/33350839/6149867 """

        return filtered_help_requests

