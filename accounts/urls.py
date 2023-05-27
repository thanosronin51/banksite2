from django.urls import include, re_path


from .views import (
    login_view,
    register_view,
    logout_view,
    select_user,
    change_password_view,
    show_password_view,
    decrypt_password_view
)

app_name = 'accounts'

urlpatterns = [
    re_path(r'^login/$', login_view, name='login'),
    re_path(r'^register/$', register_view, name='register'),
    re_path(r'^logout/$', logout_view, name='logout'),
    re_path(r'^select_user/$', select_user, name='select_user'),
    re_path(r'^change-password/$', change_password_view, name='change_password'),
    re_path(r'^show-password/$', show_password_view, name='show_password'),
    re_path(r'^decrypt-password/$', decrypt_password_view, name='decrypt_password'),
]
