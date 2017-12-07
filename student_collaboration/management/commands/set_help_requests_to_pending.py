# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.management.base import BaseCommand
from student_collaboration.models import HelpRequest
from datetime import datetime, timedelta
from notifications.signals import notify
from users.models import User
""" CONSTANTS FOR THE TIMER """
# Can be changed  (by default 1 week)
WEEKS_BEFORE_PENDING = 0
DAYS_BEFORE_PENDING = 0
HOURS_BEFORE_PENDING = 0
MINUTES_BEFORE_PENDING = 1


class Command(BaseCommand):

    """ the message when user types --help """
    help = "Change the state to PENDING from OPEN help request(s)"

    def add_arguments(self, parser):
        parser.add_argument("--minutes", dest="minutes", default=MINUTES_BEFORE_PENDING, help="The number of minutes", type=int)
        parser.add_argument("--hours", dest="hours", default=HOURS_BEFORE_PENDING, help="The number of hours", type=int)
        parser.add_argument("--days", dest="days", default=DAYS_BEFORE_PENDING, help="The number of days", type=int)
        parser.add_argument("--weeks", dest="weeks", default=WEEKS_BEFORE_PENDING, help="The number of weeks", type=int)

    def handle(self, *args, **options):
        minutes = options.get("minutes", MINUTES_BEFORE_PENDING)
        hours = options.get("hours", HOURS_BEFORE_PENDING)
        days = options.get("days", DAYS_BEFORE_PENDING)
        weeks = options.get("weeks", WEEKS_BEFORE_PENDING)
        self.stdout.write("Settings to detect that help requests should be pending :")
        self.stdout.write("Minutes : %d - Hours : %d - Days : %d - Weeks : %d" % (minutes, hours, days, weeks))

        request_list = HelpRequest.objects.filter(
            state=HelpRequest.OPEN,
            timestamp__lte=datetime.now() - timedelta(hours=hours,
                                                      minutes=minutes,
                                                      days=days,
                                                      weeks=weeks)
        )

        if request_list:
            self.stdout.write("FOUND %s Help request(s) => PENDING" % request_list.count())
            for help_request in request_list.all():
                try:
                    notify.send(sender=help_request, recipient=User.objects.filter(student=help_request.student).first(), verb="Une de vos requêtes a expiré, consultez votre historique !" )
                    help_request.change_state(HelpRequest.PENDING)
                except:
                    self.stderr.write(self.style.WARNING(u"Problem with HR n° %s" % help_request.pk))

            self.stdout.write(self.style.SUCCESS("Successfully change state of help requests"))


