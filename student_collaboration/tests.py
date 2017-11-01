# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from .models import CollaborativeSettings, StudentCollaborator, HelpRequest
from users.models import Student
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User
from skills.models import SkillHistory, Skill


# Create your tests here.
class CollaborativeSettingsTestCase(TestCase):
    def setUp(self):
        self.settings1 = CollaborativeSettings.objects.create()  # un settings par défaut
        self.settings2 = CollaborativeSettings.objects.create(distance=10)  # un settings random
        self.newuser = User.objects.create(username="jy95")
        self.student = Student.objects.create(user=self.newuser)
        """ Le StudentCollaborator associé devrait être crée """
        self.founduser = StudentCollaborator.objects.get(user=self.newuser)

    def testDistance(self):
        self.assertEqual(self.settings1.distance, CollaborativeSettings.DEFAULT_DISTANCE)
        self.assertEqual(self.settings2.distance, 10)

    def testUser(self):
        self.assertEqual(self.founduser.user.username, "jy95")
        self.assertEqual(self.founduser.settings.distance, CollaborativeSettings.DEFAULT_DISTANCE)
        self.assertEqual(self.founduser.collaborative_tool, False)

    def testChangeSettings(self):
        """ On change la distance """
        self.founduser.settings.distance = 15
        self.founduser.settings.save()
        self.assertEqual(self.founduser.settings.distance, 15)

    def testSkills(self):
        self.skill_1 = Skill.objects.create(code="B0124", name="Maths", description="Les MATHS")
        self.skill_2 = Skill.objects.create(code="B0125", name="Logique", description="La Logique")
        # reason_object1 = GenericForeignKey
        """ L'étudiant est bon en maths """
        SkillHistory.objects.create(
            skill=self.skill_1,
            student=self.founduser.user.student,
            value="acquired",
            by_who=self.founduser.user,
            reason="ACQUIS"
        )
        """ mais mauvais en logique """
        SkillHistory.objects.create(
            skill=self.skill_2,
            student=self.founduser.user.student,
            value="not acquired",
            by_who=self.founduser.user,
            reason="NULL"
        )
