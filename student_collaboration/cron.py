from .models import HelpRequest
from datetime import datetime, timedelta
import logging
logger = logging.getLogger("django_crontab")

""" CONSTANTS FOR THE TIMER """
# Can be changed  (by default 1 week)
WEEKS_BEFORE_PENDING = 0
DAYS_BEFORE_PENDING = 0
HOURS_BEFORE_PENDING = 0
MINUTES_BEFORE_PENDING = 1


def set_open_help_request_to_pending():
    """ For timedelay idea : https://stackoverflow.com/a/27869101/6149867  """
    logger.info("RUNNING CRON TASK FOR STUDENT COLLABORATION : set_open_help_request_to_pending")
    request_list = HelpRequest.objects.filter(
        state=HelpRequest.OPEN,
        timestamp__gte=datetime.now() - timedelta(hours=HOURS_BEFORE_PENDING,
                                                  minutes=MINUTES_BEFORE_PENDING,
                                                  days=DAYS_BEFORE_PENDING,
                                                  weeks=WEEKS_BEFORE_PENDING)
    )

    if request_list:
        logger.info("FOUND ", request_list.count(), "  Help request(s) => PENDING")
        for help_request in request_list.all():
            help_request.change_state(HelpRequest.PENDING)


""" CONSTANTS FOR THE TIMER """
# Can be changed (by default 2 weeks)
WEEKS_BEFORE_CLOSE = 0
DAYS_BEFORE_CLOSE = 0
HOURS_BEFORE_CLOSE = 1
MINUTES_BEFORE_CLOSE = 0


def close_pending_help_requests_automatically_when_expired():
    logger.info("RUNNING CRON TASK FOR STUDENT COLLABORATION : close_pending_help_requests_automatically_when_expired")
    request_list = HelpRequest.objects.filter(
        state=HelpRequest.PENDING,
        timestamp__gte=datetime.now() - timedelta(hours=HOURS_BEFORE_CLOSE,
                                                  minutes=MINUTES_BEFORE_CLOSE,
                                                  days=DAYS_BEFORE_CLOSE,
                                                  weeks=WEEKS_BEFORE_CLOSE)
    )
    if request_list:
        logger.info("FOUND ", request_list.count(), "  Help request(s) => CLOSED")
        for help_request in request_list.all():
            help_request.close_request()
            help_request.timestamp = datetime.now()
            help_request.save()
