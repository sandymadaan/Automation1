from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()
from Automation.tcc.models import *


urlpatterns = patterns('Automation.tcc.views',
    (r'^index/$', 'index1'),
    (r'^catalog/$', 'material'),
    (r'^previous/$', 'previous'),
    (r'^addprofile/$', 'profile'),
    (r'^performa/$', 'performa'),
    #(r'^field/$', 'field'),
    (r'^rate/$', 'rate'),
    (r'^performa/$', 'performa'),
    (r'^addjob/$', 'select'),
    (r'^save/$', 'add_job'),
    (r'^addtocart/$', 'selectcart'),
    (r'^savecart/$', 'add_to_cart'),
    (r'^search/$', 'search'),
    (r'^test-by-material-id/$', 'material_test_select'),
    #(r'^test-by-material-id/(\d+)/$', 'feed_test'),
    (r'^prev/$','previous'),
    (r'^transport/$', 'transport'),
    (r'^transportbill/$', 'transport_bill'),
    (r'^tests/$', 'tests',),
    (r'^field/(?P<field>[-\w]+)/all_json_tests/$', 'all_json_tests'),
    (r'^tags/$', 'tags'),
    (r'^tag/([-_A-Za-z0-9]+)/$','with_tag'),
    (r'^tag/([-_A-Za-z0-9]+)/page/(d+)/$', 'with_tag' ),
    (r'^removefromcart/$', 'remove_from_cart'),
    (r'^jobok/$', 'job_ok'),
    (r'^bill/$', 'bill'),
    (r'^receipt/$','receipt_report'),
    (r'^gen_report/$','gen_report'),
    (r'^report/$','rep'),
    (r'^map/$', 'displaymap'),
)

