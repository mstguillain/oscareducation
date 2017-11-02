# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from users.models import Student
from skills.models import SkillHistory, Skill
from django.db.models.signals import post_save
from django.db.models import Q
from django.dispatch import receiver
from datetime import datetime



# Create your models here.

class CollaborativeSettings(models.Model):
    """ Constante : La distance par défaut """
    DEFAULT_DISTANCE = 5
    """ Integer pour simplifier les calculs """
    distance = models.IntegerField(default=DEFAULT_DISTANCE)


class PostalCode(models.Model):

    postal_code = models.PositiveIntegerField

    longitude = models.FloatField
    latitude = models.FloatField


class StudentCollaborator(models.Model):
    # manière simple d'extend l'object user :
    #  https://docs.djangoproject.com/en/dev/topics/auth/customizing/#extending-the-existing-user-model
    user = models.OneToOneField(Student, on_delete=models.CASCADE)
    """" code postal : pour l'instant que integer"""
    postal_code = models.OneToOneField(PostalCode,null=True)
    """" flag pour dire si l'user a activé le système pour lui """
    collaborative_tool = models.BooleanField(default=False)
    """ Les settings par défaut pour ce user """
    settings = models.OneToOneField(CollaborativeSettings, on_delete=models.CASCADE)
    """" skills déjà acquises par l'user"""
    def get_mastered_skills(self):
        return SkillHistory.objects.filter(student=self.user, value="acquired").values('skill__name', 'skill__code')

    """ skills non acquises mais déjà testés """
    def get_unmastered_skills(self):
        return SkillHistory.objects.filter(student=self.user, value='not acquired').values_list('skill__id', flat=True)

    def launch_help_request(self, settings):
        return HelpRequest.objects.create(
            student=self.user,
            settings=settings
        )

    def launched_help_request_list(self):
        return HelpRequest.objects.filter(student=self.user)

    def replied_help_request_list(self):
        return HelpRequest.objects.filter(tutor=self.user)

    def change_settings(self, new_settings):
        self.settings = new_settings
        self.save()

    """ https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone """
    """ Signaux: faire en sorte qu'un objet StudentCollaborator existe si on a un modele """
    @receiver(post_save, sender=Student)
    def create_student_collaborator_profile(sender, instance, created, **kwargs):
        if created:
            """ On crée effectivement notre profile """
            StudentCollaborator.objects.create(
                user=instance,
                collaborative_tool=False,
                settings=CollaborativeSettings.objects.create()  # Initialisé avec les settings par défaut
            )


class HelpRequest(models.Model):
    """ Constantes : status des demandes """
    CLOSED = "Closed"
    OPEN = "Open"
    ACCEPTED = u"Accepted"
    PENDING = u"Pending"
    """ date et heure de création """
    timestamp = models.DateTimeField(default=datetime.now)

    """ Les settings pour cette demande """
    settings = models.ForeignKey(CollaborativeSettings)

    """ L'état actuel de la requête """
    requestStatus = (
        (CLOSED, u"Cloturé"),
        (OPEN, "Ouverte"),
        (ACCEPTED, u"Accepté"),
        (PENDING, "Timer expired"),
    )
    state = models.CharField(max_length=20, null=False, choices=requestStatus, default=OPEN)
    """ La compétence qui est l'objet de l'aide """
    skill = models.ManyToManyField(Skill)
    """ L'étudiant qui aide ; pas présent au début """
    tutor = models.ForeignKey(Student, null=True, related_name="%(class)s_tutor")
    """ L'étudiant qui a demandé de l'aide """
    student = models.ForeignKey(Student)

    """ Le commentaire laissé à la fin de l'aide """
    """ Par défaut , un message auto du système """
    DEFAULT_COMMENT = u"Fermé par le système"
    comment = models.CharField(max_length=255, null=True)

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
    closedReason = models.CharField(max_length=255, null=True, choices=closedCategories)

    """ Permet de répondre à une help request ouverte """
    def reply_to_unanswered_help_request(self, user):
        """ L'étudiant qui répond est le tuteur """
        self.tutor = user
        """ On passe l'état à En cours """
        self.state = HelpRequest.ACCEPTED
        self.save()

    def close_request(self, comment, close_category):
        self.state = HelpRequest.CLOSED
        """ Si on a fourni un commentaire """
        if comment is not None:
            self.comment = comment
        else:
            self.comment = HelpRequest.DEFAULT_COMMENT
        """ Si on a fourni une autre category que celle par défaut """
        if close_category is not None:
            self.closedReason = close_category
        else:
            self.closedReason = HelpRequest.CLOSED_BY_SYSTEM
        self.save()

    def change_settings(self, new_settings):
        self.settings = new_settings
        self.save()

    def change_state(self, new_state):
        self.state = new_state
        self.save()

    """ Signal : Quand compétence maitrisé, on ferme auto la help request """
    @receiver(post_save, sender=SkillHistory)
    def check_status(sender, instance, **kwargs):
        if instance.value == 'acquired':
            """ On récupère les help request qui doivent être fermé """
            helprequest_to_be_closed = HelpRequest.objects.filter(
                student=instance.student,
                skill=instance.skill,
            ).exclude(
                state=HelpRequest.CLOSED
            )
            """ Si trouvé, on les ferme """
            if not helprequest_to_be_closed:
                for closed in helprequest_to_be_closed.all():
                    closed.close_request()

