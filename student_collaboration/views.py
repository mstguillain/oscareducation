# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from student_collaboration.models import StudentCollaborator, CollaborativeSettings, HelpRequest
from users.models import Student
from skills.models import Skill
from .forms import StudentCollaboratorFormCollaborativeTool, StudentCollaboratorFormPostalCode, CollaborativeSettingsForm, UnmasteredSkillsForm, HelpRequestForm
from math import sin, cos, sqrt, atan2, radians
from decorators import user_has_collaborative_tool_active

# Create your views here.
@login_required
def update_settings(request):
    # requête de type POST; on update
    true_student = get_object_or_404(Student, user=request.user.pk)
    student = get_object_or_404(StudentCollaborator, pk=true_student.studentcollaborator.pk)

    if request.method == 'POST':
        settings = get_object_or_404(CollaborativeSettings, pk=true_student.studentcollaborator.settings.pk)
        settings_form = CollaborativeSettingsForm(request.POST, instance=settings)
        student_form_collaborative_tool = StudentCollaboratorFormCollaborativeTool(request.POST, instance=student)
        student_form_postal_code = StudentCollaboratorFormPostalCode(request.POST, instance=student)

        if student_form_collaborative_tool.is_valid() and student_form_postal_code.is_valid() and settings_form.is_valid():
            settings = settings_form.save(commit=False)

            student = student_form_collaborative_tool.save(commit=False)
            student.save()

            student = student_form_postal_code.save(commit=False)
            student.save()

            student_form_collaborative_tool.settings = settings
            settings.save()

            student_form_postal_code.settings = settings
            settings.save()

            return HttpResponseRedirect('/student_collaboration/settings/')

    else:
        # l'user peut avoir ou n'a pas de settings
        #L'ANGLAIS OMGGGGGG
        settings_pk = None
        if true_student.studentcollaborator.settings:
            settings_pk = true_student.studentcollaborator.settings.pk
        settings, is_created = CollaborativeSettings.objects.get_or_create(
            pk=settings_pk
        )
        # settings just created ; add them to user
        if is_created:
            student.settings = settings
            student.save()

        settings_form = CollaborativeSettingsForm(instance=settings)
        student_form_collaborative_tool = StudentCollaboratorFormCollaborativeTool(instance=student)
        student_form_postal_code = StudentCollaboratorFormPostalCode(instance=student)
        return render(request, 'student_collaboration/student_settings.haml', {
            'student_form_collaborative_tool': student_form_collaborative_tool,
            'student_form_postal_code': student_form_postal_code,
            'settings_form': settings_form
        })


@login_required
@user_has_collaborative_tool_active
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
@user_has_collaborative_tool_active
def open_help_request(request, id=None):
    if id:
        hp = HelpRequest.objects.filter(id=id).first()
        hp.reply_to_unanswered_help_request(request.user.student)

    """ On redirige vers la list view """
    return redirect('provide_help')


@login_required
def collaborative_home(request):
    return render(request, 'student_collaboration/student_collaboration_home.haml')


def help_request_hist(request, status=None, id=None):
    if status == "provide":
        print("hello")
    if status == "closed":
        if id:
            hp = HelpRequest.objects.filter(id=id).first()
            hp.close_request(None,None)
    return redirect('help_request_history')


class HelpRequestHistory(ListView):
    model = HelpRequest
    template_name = "student_collaboration/help_request_history.haml"
    context_object_name = "open_help_requests"

    def get_context_data(self, **kwargs):
        context = super(HelpRequestHistory, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        """We recover help request from User"""
        #if self.status == "provide":
        #    open_help_requests = HelpRequest.objects.filter(tutor=self.request.user.student)
        #else:
        open_help_requests = HelpRequest.objects.filter(student=self.request.user.student)
        print(HelpRequestHistory)
        return open_help_requests


@method_decorator(login_required, name='dispatch')
@method_decorator(user_has_collaborative_tool_active, name='dispatch')
class OpenHelpRequestsListView(ListView):
    model = HelpRequest
    paginate_by = 10
    template_name = "student_collaboration/open_help_requests_list.haml"
    context_object_name = "open_help_requests"

    def dispatch(self, *args, **kwargs):
        return super(OpenHelpRequestsListView,self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(OpenHelpRequestsListView, self).get_context_data(**kwargs)
        context['currentUserPk'] = self.request.user.student.studentcollaborator.pk
        return context

    def get_queryset(self):
        """ On cherche les compétences maitrisées de l'aidant """
        # et l'anglais????
        mastered_skill_list = self.request.user.student.studentcollaborator.get_mastered_skills()
        open_help_requests = HelpRequest.objects.filter(
            state=HelpRequest.OPEN,
            skill__in=mastered_skill_list
        )
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


