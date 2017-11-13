from .models import HelpRequest
from datetime import datetime, timedelta

""" CONSTANTES POUR TIMER """
# A changer selon ses envies (par defaut 1 semaine)
WEEKS_BEFORE_PENDING = 0
DAYS_BEFORE_PENDING = 0
HOURS_BEFORE_PENDING = 0
MINUTES_BEFORE_PENDING = 3


def set_open_help_request_to_pending():
    """ For timedelay idea : https://stackoverflow.com/a/27869101/6149867  """
    print u"RUNNING CRON TASK FOR STUDENT COLLABORATION"
    request_list = HelpRequest.objects.filter(
        state=HelpRequest.OPEN,
        timestamp__gte=datetime.now()-timedelta(hours=HOURS_BEFORE_PENDING,
                                                minutes=MINUTES_BEFORE_PENDING,
                                                days=DAYS_BEFORE_PENDING,
                                                weeks=WEEKS_BEFORE_PENDING)
    )
    if not request_list:
        for help_request in request_list.all():
            help_request.change_state(HelpRequest.PENDING)
            help_request.timestamp = datetime.now()
            help_request.save()

""" CONSTANTES POUR TIMER """
# A changer selon ses envies (par defaut 2 semaine)
WEEKS_BEFORE_CLOSE = 0
DAYS_BEFORE_CLOSE = 0
HOURS_BEFORE_CLOSE = 1
MINUTES_BEFORE_CLOSE = 0


def close_pending_help_requests_automatically_when_expired():
    print u"RUNNING CRON TASK 2 FOR STUDENT COLLABORATION"
    request_list = HelpRequest.objects.filter(
        state=HelpRequest.PENDING,
        timestamp__gte=datetime.now()-timedelta(hours=HOURS_BEFORE_CLOSE,
                                                minutes=MINUTES_BEFORE_CLOSE,
                                                days=DAYS_BEFORE_CLOSE,
                                                weeks=WEEKS_BEFORE_CLOSE)
    )
    if not request_list:
        for help_request in request_list.all():
            help_request.change_state(HelpRequest.CLOSED)
            help_request.timestamp = datetime.now()
            help_request.save()

