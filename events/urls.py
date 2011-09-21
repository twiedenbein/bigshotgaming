from django.conf.urls.defaults import *
# from events.forms import RegisterForm1, RegisterForm2, RegisterForm3, RegisterWizard



urlpatterns = patterns('events.views',
    (r'^$', 'index', {}, 'events_index'),
    # fix me
    # 
    (r'^register/(\d+)/$', 'register', {}, 'events_register'),
    (r'^participants/(\d+)/', 'participants', {}, 'events_participants'),
    (r'^payment/', 'payment', {}, 'events_payment'),
    (r'^activate/(\d+)/([\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/', 'activate', {}, 'events_activate'),
    (r'^ppnotification', include('paypal.standard.ipn.urls')), 
)