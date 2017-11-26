from django.conf.urls import url,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.index,name='index'),
    url(r'^$', views.homepage,name='home'),
    url(r'^profiles/$', views.profile,name='profiles'),
    url(r'^profiles/post', views.posts,name='uploadpost'),
    url(r'^profiles/edit', views.update_profile,name='editprofile'),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
