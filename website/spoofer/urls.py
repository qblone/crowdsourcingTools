from django.conf.urls import url

from . import views
from . import views.MyView as MyView

urlpatterns = [
    url(r'^$', MyView.as_view()),

 #       url(r'^$', views.index, name='index'),
]
