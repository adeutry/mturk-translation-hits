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
            'worker_id': request.GET.get("workerId", "None"),
            'assignment_id' : request.GET.get("assignmentId", "None"),
            'amazon_host' : "https://www.mturk.com/mturk/externalSubmit",
            'in_dev' : request.GET.get("dev", "None"),
            'hit_id' : request.GET.get("hitId", "None"),
            }

    context['in_dev'] = (context['in_dev'] == "True")

    # set external submit url
    if context['in_dev']:
        context['amazon_host'] = SUBMIT_URL_DEV
    else:
        context['amazon_host'] = SUBMIT_URL_PROD

    res = render(request, 'mturk/paraphrase.html', context)
    res['x-frame-options'] = 'do you like memes?'
    return res 

def get_rtt(request):
    text = request.GET.get("text", "None")
    import utils.utils
    rtt = utils.rtt(text, "de")
    return HttpResponse(rtt)

def get_paraphrase_sents(request):
    trans = Translation.objects.filter(
        group=1
    ).filter(
        grade_level='12.0'
    )
    
    trans_json = [t.to_json() for t in trans]
    return HttpResponse(json.dumps(trans_json))


