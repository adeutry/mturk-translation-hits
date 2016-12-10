from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from ..models import Sentence, Translation, Paraphrase
import pdb, random, json
import logging

SUBMIT_URL_DEV =  "https://workersandbox.mturk.com/mturk/externalSubmit"
SUBMIT_URL_PROD = "https://www.mturk.com/mturk/externalSubmit"

def index(request):
    
    # prepare the context
    context = {
            'in_dev' : request.GET.get("dev", "None"),
            'username' : request.GET.get("username", "None")
            }

    context['in_dev'] = (context['in_dev'] == "True")

    if context['username'] != "None":
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
    trans = Translation.objects.filter(
        group=1
    ).filter(
        grade_level='12.0'
    )
    
    # serialize translations
    trans_json = [t.to_json() for t in trans]

    # shuffle the translations
    random.shuffle(trans_json)

    return HttpResponse(json.dumps(trans_json[:5]))


def store_answer_data(request):
    answer_data_json = request.POST.get("answerData", "None")
    answer_username = request.POST.get("username", "None")
    answer_data = json.loads(answer_data_json)
    for answer in answer_data:
        paraphrase = Paraphrase(
            original_text = answer['original'],
            paraphrase_text= answer['paraphrase'],
            trans_id = answer['trans_id'],
            username = answer_username
            )
        paraphrase.save()
    return JsonResponse(answer_data_json, safe=False)

def complete(request):
    return render(request, 'mturk/paraphrase_complete.html')
