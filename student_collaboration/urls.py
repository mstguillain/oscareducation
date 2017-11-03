from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    # exemple de view : views.update_settings
    # exemple de ligne : url(r'^dashboard/$', views.dashboard, name='student_dashboard'),
    url(r'^$', views.collaborative_home, name='collaborative_home'),
    url(r'^settings/$', views.update_settings, name='settings'),
    url(r'^request_help/$', views.submit_help_request, name='request_help'),
    url(r'^provide_help/$', views.open_help_request, name='provide_help'),
    url('^provide_help/([0-9]+)$', views.open_help_request, name='reply_help'),
]
