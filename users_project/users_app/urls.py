from django.conf.urls import url
from users_app import views

# Template URLs
app_name = 'users_app'

urlpatterns = [
    url(r'^user_login/$', views.user_login, name='user_login'),
    url(r'^user_logout/$', views.user_logout, name='user_logout'),
    url(r'^user_logged_in/$', views.user_logged_in, name='user_logged_in'),
    url(r'^register/$', views.register, name='register'),
]
