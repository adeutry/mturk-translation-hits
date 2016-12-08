from django.shortcuts import render
from django.http import HttpResponse
from ..models import Sentence, Translation
import pdb, random, json
import logging

SUBMIT_URL_DEV =  "https://workersandbox.mturk.com/mturk/externalSubmit"
SUBMIT_URL_PROD = "https://www.mturk.com/mturk/externalSubmit"

def index(request):
    
    sents = Sentence.objects.all()
    sent = random.sample(list(sents), 1)[0]
    # prepare the context
    context = {
            'in_dev' : request.GET.get("dev", "None"),
            'username' : request.GET.get("username", "None")
            }

    context['in_dev'] = (context['in_dev'] == "True")

    res = render(request, 'mturk/paraphrase.html', context)
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

    return HttpResponse(json.dumps(trans_json))


