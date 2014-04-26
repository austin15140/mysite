from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static

from users import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<user_id>\d+)/detail/$', views.detail, name='detail'),
    url(r'^(?P<user>[\w+.])/download/$', views.download_img, name='dl_img'),
    url(r'^language/(?P<language>[a-z\-]+)/$', views.language, name='language'),
    url(r'^login/$', views.user_login, name='u_login'),
    url(r'^(?P<user_id>\d+)/success/$', views.user_login_success, name='u_success'),
    url(r'^/logout/$', views.user_logout, name='u_logout'),

)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)