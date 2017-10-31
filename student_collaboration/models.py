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
    """ Les settings par défaut pour ce user """
    settings = models.ForeignKey(CollaborativeSettings)
    """" skills déjà acquises par l'user"""
    def get_mastered_skills(self):
        return SkillHistory.objects.filter(student=self.user, value="acquired").values('skill__name', 'skill__code')

    """ skills non acquises mais déjà testés """
    def get_unmastered_skills(self):
        return SkillHistory.objects.filter(student=self.user, value='not acquired').values('skill__name', 'skill__code')

    def launch_help_request(self, skill_requested, settings):
        HelpRequest.objects.create(
            student=self.user,
            skill=skill_requested,
            settings=settings
        )

    def launched_help_request_list(self):
        return HelpRequest.objects.filter(student=self.user)

    def replied_help_request_list(self):
        return HelpRequest.objects.filter(tutor=self.user)


class HelpRequest(models.Model):
    """ Constantes : status des demandes """
    CLOSED = "Closed"
    OPEN = "Open"
    PENDING = "Pending"

    timestamp = models.DateTimeField(default=datetime.now)
    """ L'état actuel de la requête """
    requestStatus =  (
        (CLOSED, u"Cloturé"),
        (OPEN, "Ouverte"),
        (PENDING, "En cours"),
    )
    state = models.CharField(max_length=20, null=False, choices=requestStatus, default=OPEN)
    """ La compétence qui est l'objet de l'aide """
    skill = models.ForeignKey(Skill)
    """ L'étudiant qui aide ; pas présent au début """
    tutor = models.ForeignKey(User, null=True)
    """ L'étudiant qui a demandé de l'aide """
    student = models.ForeignKey(User)

    """ Le commentaire laissé à la fin de l'aide """
    """ Par défaut , un message auto du système """
    DEFAULT_COMMENT = u"Fermé par le système"
    comment = models.CharField(max_length=255, default=DEFAULT_COMMENT)

    """ les categories possibles d'une cloture; ici volontaire restreint pour update à l'avenir """
    CLOSED_BY_SYSTEM = "SYSTEM_CLOSED"
    CANNOT_HELP = "CANNOT_HELP"
    TRIED_TO_HELP = "TRIED_TO_HELP"

    closedCategories = (
        (CLOSED_BY_SYSTEM, u"Cloturé par le système"),
        (CANNOT_HELP, u"Ne sait pas aider"),
        (TRIED_TO_HELP, u"A aidé dans la mesure du possible")
    )
    """ La raison de la fin de la help request """
    closedReason = models.CharField(max_length=255, null=False, choices=closedCategories, default=CLOSED_BY_SYSTEM)

    """ Permet de répondre à une help request ouverte """
    def reply_to_unanswered_help_request(self, user):
        """ L'étudiant qui répond est le tuteur """
        self.tutor = user
        """ On passe l'état à En cours """
        self.state = HelpRequest.PENDING
        self.save()

    def close_request(self, comment, closeCategory):
        self.state = HelpRequest.CLOSED
        """ Si on a fourni un commentaire """
        if comment is not None:
            self.comment = comment
        """ Si on a fourni une autre category que celle par défaut """
        if closeCategory is not None:
            self.closedReason = closeCategory
        self.save()


class CollaborativeSettings(models.Model):
    """ Constante : La distance par défaut """
    DEFAULT_DISTANCE = 5
    """ Integer pour simplifier les calculs """
    distance = models.IntegerField(default=DEFAULT_DISTANCE)
