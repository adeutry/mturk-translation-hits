from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^get_sent$', views.get_sent, name='get_sent'),
        url(r'^get_trans$', views.get_trans, name='get_trans'),
        url(r'^get_hit_questions$', views.get_hit_questions, name='get_hit_questions')
        ]
