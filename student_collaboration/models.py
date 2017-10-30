# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from skills.models import SkillHistory,Skill
from datetime import datetime


# Create your models here.
# L'extension de l'user ; à compléter
class StudentCollaborator(models.Model):
    # manière simple d'extend l'object user :
    #  https://docs.djangoproject.com/en/dev/topics/auth/customizing/#extending-the-existing-user-model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    """" code postal : pour l'instant que integer"""
    code_postal = models.IntegerField()
    """" flag pour dire si l'user a activé le système pour lui """
    collaborative_tool = models.BooleanField(default=False)

    """" skills déjà acquises par l'user"""
    """ à checker si correct ; devrait retourner une liste d'ID (1,2,3,etc) """

    def get_skills(self):
        return SkillHistory.objects.filter(student=self.user, value="acquired").values_list('skill')

    def launch_help_request(self, skill_requested, settings):
        """ //TODO """

    def reply_help_request(self, help_request):
        """ //TODO """

    def launched_help_request_list(self):
        return HelpRequest.objects.filter(student=self.user)

    def replied_help_request_list(self):
        return HelpRequest.objects.filter(tutor=self.user)


class HelpRequest(models.Model):
    timestamp = models.DateTimeField(default=datetime.now)
    """ L'état actuel de la requête """
    state = models.CharField(max_length=20, null=False, blank=False, choices=(
        ("Closed", "Cloturé"),
        ("Open", "Ouverte"),
        ("Pending", "En cours"),
    ))
    """ La compétence qui est l'objet de l'aide """
    skill = models.ForeignKey(Skill)
    """ L'étudiant qui aide """
    tutor = models.ForeignKey(User)
    """ L'étudiant qui a demandé de l'aide """
    student = models.ForeignKey(User)
