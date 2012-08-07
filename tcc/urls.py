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
    (r'^add_job/$', 'field_test_select'),
    #(r'^test-by-field-id/(\d+)/$', 'feed_models'),
    #(r'^prev/$',''),
    (r'^tests/$', 'tests',),
    (r'^field/(?P<field>[-\w]+)/all_json_tests/$', 'all_json_tests'),
)

