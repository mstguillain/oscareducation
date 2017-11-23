# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from .models import CollaborativeSettings, StudentCollaborator, HelpRequest, PostalCode
from users.models import Student
from django.contrib.auth.models import User
from skills.models import SkillHistory, Skill
# Just to simulate the signal send by promotion view
from promotions.signals import student_added_to_lesson
from promotions.models import Lesson


# Create your tests here.
class CollaborativeSettingsTestCase(TestCase):
    def setUp(self):
        self.settings1 = CollaborativeSettings.objects.create()  # un settings par défaut
        self.settings2 = CollaborativeSettings.objects.create(distance=10)  # un settings random
        """ The student who is going to ask help  """
        self.newuser = User.objects.create(username="jy95")
        self.student = Student.objects.create(user=self.newuser)
        student_added_to_lesson.send(sender=Lesson, student=self.student, level=StudentCollaborator.MINIMAL_DEGREE)
        # add a settings just to make tests easy
        StudentCollaborator.objects.filter(user=self.student).update(settings=self.settings1)
        self.founduser = StudentCollaborator.objects.get(user=self.student)
        """ A random skill """
        self.skill_1 = Skill.objects.create(code="B0124", name="Maths", description="Les MATHS")
        """ The student who is going to accept the help request """
        self.newuser2 = User.objects.create(username="OscarLeGrandFrere")
        self.student2 = Student.objects.create(user=self.newuser2)
        student_added_to_lesson.send(sender=Lesson, student=self.student2, level=StudentCollaborator.MINIMAL_DEGREE)
        # add a settings just to make tests easy
        StudentCollaborator.objects.filter(user=self.student2).update(settings=self.settings2)
        self.founduser2 = StudentCollaborator.objects.get(user=self.student2)

    def testDistance(self):
        self.assertEqual(self.settings1.distance, CollaborativeSettings.DEFAULT_DISTANCE)
        self.assertEqual(self.settings2.distance, 10)

    def testUser(self):
        self.assertEqual(self.founduser.user.user.username, "jy95")
        self.assertEqual(self.founduser.collaborative_tool, False)

    def testChangeSettings(self):
        """ On change la distance """
        self.founduser.settings.distance = 15
        self.founduser.settings.save()
        self.assertEqual(self.founduser.settings.distance, 15)

    def testSkills(self):
        # reason_object1 = GenericForeignKey
        """ L'étudiant est bon en maths """
        # SkillHistory.objects.create(
        #    skill=self.skill_1,
        #    student=self.founduser.user.student,
        #    value="acquired",
        #    by_who=self.founduser.user,
        #    reason="ACQUIS"
        # )
        """ mais mauvais en logique """
        # SkillHistory.objects.create(
        #     skill=self.skill_2,
        #     student=self.founduser.user.student,
        #     value="not acquired",
        #     by_who=self.founduser.user,
        #     reason="NULL"
        # )

    def testCreateHelpRequest(self):
        skill_2 = Skill.objects.create(code="B0125", name="Logique", description="La Logique")
        help_request = self.founduser.launch_help_request(self.founduser.settings)
        help_request.skill.add(skill_2)
        help_request = HelpRequest.objects.get(student=self.founduser.user, skill=skill_2)
        self.assertEqual(help_request.student, self.founduser.user)
        self.assertTrue(help_request.skill.filter(pk=skill_2.pk).exists())
        self.assertIsNone(help_request.tutor)
        self.assertEqual(help_request.state, HelpRequest.OPEN)
        self.assertEqual(help_request.settings, self.founduser.settings)

    def testStateForHelpRequest(self):
        skill_2 = Skill.objects.create(code="B0125", name="Logique", description="La Logique")
        """ We create the fake help request """
        help_request = self.founduser.launch_help_request(self.founduser.settings)
        help_request.skill.add(skill_2)
        """ We fetch the help request we just created """
        help_request = HelpRequest.objects.get(student=self.founduser.user, skill=skill_2)
        """ User OscarLeGrandFrere accepts the help request """
        help_request.reply_to_unanswered_help_request(self.founduser2.user)
        help_request = HelpRequest.objects.get(student=self.founduser.user, skill=skill_2)
        self.assertEqual(help_request.student, self.founduser.user)
        self.assertTrue(help_request.skill.filter(pk=skill_2.pk).exists())
        self.assertEqual(help_request.state, HelpRequest.ACCEPTED)
        """ We change the state; for example when the help request has expired """
        help_request.change_state(HelpRequest.PENDING)
        help_request = HelpRequest.objects.get(student=self.founduser.user, skill=skill_2)
        self.assertEqual(help_request.state, HelpRequest.PENDING)
        """ We close the help request """
        comment = u"J'ai fourni des explications que je juge suffisante"
        help_request.close_request(comment, HelpRequest.TRIED_TO_HELP)
        help_request = HelpRequest.objects.get(student=self.founduser.user, skill=skill_2)
        self.assertEqual(help_request.state, HelpRequest.CLOSED)
        self.assertEqual(help_request.closedReason, HelpRequest.TRIED_TO_HELP)
        self.assertEqual(help_request.comment, comment)
