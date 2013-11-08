import os
from django.views.generic import TemplateView
from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from PassManagerApp.views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

site_media = os.path.join(
                          os.path.dirname(__file__), 'site_media'
                          )
urlpatterns = patterns('',
    # Browsing
    (r'^$', main_page),
    (r'^user/(\w+)/$', user_page),
    # Session management
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', logout_page),
    (r'^register/$', register_page),
    (r'^register/success/$', TemplateView.as_view(template_name="registration/register_success.html")),
    # Account management
    (r'^save/$', login_save_page),
    (r'^edit/$', login_edit_page),
    (r'^delete/$', login_delete_page),
    # Site media
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': site_media}),
    )
