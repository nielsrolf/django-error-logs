from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^list$', views.all_errors),
]

urlpatterns = format_suffix_patterns(urlpatterns)