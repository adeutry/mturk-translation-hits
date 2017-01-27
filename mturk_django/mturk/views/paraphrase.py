from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from ..models import Sentence, Translation, Paraphrase
import pdb, random, json
import logging

def index(request):
    
    # prepare the context
    context = {
            'in_dev' : request.GET.get("dev", "None"),
            'username' : request.GET.get("username", "None")
            }

    context['in_dev'] = (context['in_dev'] == "True")

    if context['username'] != "None":
        ''' initialize the session for the user'''

        # set session values
        request.session['username'] = context['username']

        res = render(request, 'mturk/paraphrase.html', context)
    else:
        res = render(request, 'mturk/paraphrase_login.html', context)

    res['x-frame-options'] = 'do you like memes?'

    return res 

def get_rtt(request):
    text = request.GET.get("text", "None")
    from .utils import utils
    rtt = utils.rtt(text, "de", sleep=0.0)
    return HttpResponse(rtt)

def get_paraphrase_sents(request):

    # these are the worst 12th grade translations rated by turkers
    trans_ids = [611, 811, 781, 91, 151, 241, 671, 451, 81, 801, 381, 631, 641, 791, 731]

    # load worst translations from db
    trans = Translation.objects.filter(
            id__in=trans_ids
    )    

    # serialize translations
    trans_json = [t.to_json() for t in trans]

    # shuffle the translations
    random.shuffle(trans_json)

    return HttpResponse(json.dumps(trans_json))


def store_answer_data(request):
    username = request.session.get('username', False)
    if username:
        # logging
        logger = logging.getLogger('mturk')

        answer_data_json = request.POST.get("answerData", "None")
        answer = json.loads(answer_data_json)

        logger.debug(answer_data_json)

        paraphrase = Paraphrase(
            original_text = answer['original'],
            paraphrase_text = answer['paraphrase'],
            time = answer['time'],
            trans_id = answer['trans_id'],
            order  = answer['order'],
            username = username
        )

        paraphrase.save()
        return JsonResponse(answer_data_json, safe=False)
    else:
        return HttpResponse(status=401, reason="username not defined in session")

def complete(request):
    return render(request, 'mturk/paraphrase_complete.html')
