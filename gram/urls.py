from django.conf.urls import url,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.index,name='index'),
    url(r'^$', views.homepage,name='home'),
    url(r'^profiles/(?P<username>[-_\w.]+)$', views.profile,name='profiles'),
    url(r'^profiles/post/$', views.posts,name='uploadpost'),
    url(r'^profiles/edit/(?P<username>[-_\w.]+)$', views.update_profile,name='editprofile'),
    url(r'^update-profile-picture/(?P<username>[-_\w.]+)$', views.profile_pic_update, name='update_profilepic'),
    url(r'^(?P<slug>[\w\-]{10})/like/$',views.like_post_view,name='like'),
    url(r'^(?P<slug>[\w\-]{10})/unlike/$',views.unlike_post_view,name='unlike'),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
