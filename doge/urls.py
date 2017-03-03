"""doge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from doge import settings
from django.contrib.staticfiles import views
from myapp import views as m_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', m_views.index, name='index'),
    url(r'^signup/', m_views.signup, name='signup'),
    url(r'^signdown/', m_views.signdown, name='signdown'),
    url(r'^login/', m_views.login, name='login'),
    url(r'^all/', m_views.all, name='all'),
    url(r'^query/$', m_views.query, name='query'),
]


if settings.DEBUG:
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', views.static.serve, {'document_root': settings.STATIC_ROOT}, name="static"),
        url(r'^media/(?P<path>.*)$', views.static.serve, {'document_root': settings.MEDIA_ROOT}, name="media")
    ]
