from django.urls import include, re_path

from .views import *

app_name = 'transactions'

urlpatterns = [
    # re_path(r'^$', home_view, name='home'),
    re_path(r'^deposit/$', deposit_view, name='deposit'),
    re_path(r'^withdrawal/$', withdrawal_view, name='withdrawal'),
    re_path(r'^Withdrawal_international_view/$', Withdrawal_international_view, name='Withdrawal_international_view'),
    re_path(r'^loan_request/$', loan_request_view, name='loan_request'),
    re_path(r'^create/$', payment_create, name='payment_create'),
    re_path(r'^success/$', payment_success, name='payment_success'),
    re_path(r'^recent_withdrawals/$', recent_withdrawals, name='recent_withdrawals'),
    re_path(r'^recent_international_withdrawals/$', recent_international_withdrawals, name='recent_international_withdrawals'),
    re_path(r'^recent_payments/$', recent_payments, name='recent_payments'),

]
