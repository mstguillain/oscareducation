from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    # exemple de view : views.update_settings
    # exemple de ligne : url(r'^dashboard/$', views.dashboard, name='student_dashboard'),
    url(r'^$', views.collaborative_home, name='collaborative_home'),
    url(r'^settings/$', views.update_settings, name='settings'),
    url(r'^request_help/$', views.submit_help_request, name='request_help'),
    url(r'^provide_help/$', views.OpenHelpRequestsListView.as_view(), name='provide_help'),
    url('^provide_help/([0-9]+)$', views.open_help_request, name='reply_help'),
    url(r'^help_request_history/$', views.HelpRequestHistory.as_view(), name = 'help_request_history'),
    url(r'^help_request_history/(?P<status>[\w\-]+)/(?P<id>[0-9]+)$', views.help_request_hist,name = 'change_history')
]
