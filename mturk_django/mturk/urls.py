from django.conf.urls import url

from . import views
from . import adequacy

urlpatterns = [
        url(r'^fluency_1$', views.index, name='index'),
        url(r'^fluency_1/get_sent$', views.get_sent, name='get_sent'),
        url(r'^fluency_1/get_trans$', views.get_trans, name='get_trans'),
        url(r'^fluency_1/get_hit_questions$', views.get_hit_questions, name='get_hit_questions'),
        url(r'^fluency_1.*', views.index, name='index'),
        url(r'^adequacy_1$', adequacy.index, name='index'),
        url(r'^adequacy_1/get_sent$', adequacy.get_sent, name='get_sent'),
        url(r'^adequacy_1/get_trans$', adequacy.get_trans, name='get_trans'),
        url(r'^adequacy_1/get_hit_questions$', adequacy.get_hit_questions, name='get_hit_questions'),
        url(r'^adequacy_1.*', adequacy.index, name='index'),
        ]
