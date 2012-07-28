from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()
from Automation.tcc.models import *

urlpatterns = patterns('Automation.tcc.views',
    (r'^index/$', 'index1'),
    (r'^catalog/$', 'catalog'),
    (r'^previous/$', 'previous'),
    (r'^addprofile/$', 'profile'),
    (r'^performa/$', 'performa'),
    (r'^field/$', 'field'),
    (r'^rate/$', 'rate'),
    (r'^performa/$', 'performa'),
    (r'^add_job/$', 'add_job'),
    (r'^lab/(?P<lab>[-\w]+)/all_tcc_fields/$', 'all_tcc_fields'),
    (r'^tests/$', 'tests',),
)
