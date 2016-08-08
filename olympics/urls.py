from olympics import views
from django.conf.urls import url

urlpatterns = [
    url('^$', views.index)
]
