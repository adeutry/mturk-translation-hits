from django.conf.urls import url

from .views import fluency
from .views import adequacy
from .views import adequacy_multi
from .views import paraphrase

urlpatterns = [
        url(r'^fluency_1$', fluency.index, name='index'),
        url(r'^fluency_1/get_sent$', fluency.get_sent, name='get_sent'),
        url(r'^fluency_1/get_trans$', fluency.get_trans, name='get_trans'),
        url(r'^fluency_1/get_hit_questions$', fluency.get_hit_questions, name='get_hit_questions'),
        url(r'^fluency_1.*', fluency.index, name='index'),
        url(r'^adequacy_1$', adequacy.index, name='index'),
        url(r'^adequacy_1/get_sent$', adequacy.get_sent, name='get_sent'),
        url(r'^adequacy_1/get_trans$', adequacy.get_trans, name='get_trans'),
        url(r'^adequacy_1/get_hit_questions$', adequacy.get_hit_questions, name='get_hit_questions'),
        url(r'^adequacy_1.*', adequacy.index, name='index'),
        url(r'^adequacy_multi$', adequacy_multi.index, name='index'),
        url(r'^adequacy_multi/get_hit_questions$', adequacy_multi.get_hit_questions, name='get_hit_questions'),
        url(r'^paraphrase_1$', paraphrase.index, name='index'),
        url(r'^paraphrase_1/get_rtt$', paraphrase.get_rtt, name='get_rtt'),
        url(r'^paraphrase_1/get_paraphrase_sents$', paraphrase.get_paraphrase_sents, name='get_paraphrase_sents'),
        url(r'^paraphrase_1/submit_answer$', paraphrase.store_answer_data, name='submit_paraphrase'),
        url(r'^paraphrase_1/complete$', paraphrase.complete, name='paraphrase_complete')
        ]
