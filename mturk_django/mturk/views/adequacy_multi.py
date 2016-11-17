from django.shortcuts import render
from django.http import HttpResponse
from ..models import Sentence, Translation
import pdb, random, json
import logging

SUBMIT_URL_DEV =  "https://workersandbox.mturk.com/mturk/externalSubmit"
SUBMIT_URL_PROD = "https://www.mturk.com/mturk/externalSubmit"
CURRENT_TRANS_GROUP = 2
CURRENT_TRANS_LANG = "chi"
NUM_GENUINE = 12
NUM_REPEAT = 3
NUM_GOOD_REFS = 5

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

    res = render(request, 'mturk/adequacy_multi.html', context)
    res['x-frame-options'] = 'do you like memes?'
    return res 

def get_sent(request):
    sents = Sentence.objects.all()
    sent = random.sample(list(sents), 1)[0]
    return HttpResponse(sent.text)

def get_trans(request):
    all_trans = Translation.objects.all()
    trans = random.sample(list(all_trans), 1)[0]
    return HttpResponse(trans.trans_text)
 
def get_hit_questions(request):
    '''
    Get the HIT questions for the adequacy HIT with multiple translations.
    This hit differs from the original adequacy HIT in that instead of showing
    a single translation next to the original sentence, the HIT shows the 
    original 12th grade sentence and three translations, one for 12th grade,
    9th grade, and 7th grade.
    '''
    logger = logging.getLogger("mturk")

    # the list of all the individual translations used for each question
    # we need this later to pick good references
    trans = list()

    # the list of all questions. Each contains the original sentence and
    # a list of three translations.
    questions = list()

    # only load the translations in our translation groups and language
    all_trans = (Translation.objects
            .filter(group=CURRENT_TRANS_GROUP)
            .filter(trans_lang=CURRENT_TRANS_LANG))
    all_trans_list = list(all_trans)

    # get the align ids of the translations and randomly sample them
    all_align_ids = [t.align_id for t in all_trans_list]
    rand_align_ids = random.sample(all_align_ids, NUM_GENUINE)

    # construct the questions objects
    for align_id in rand_align_ids:
        align_trans = all_trans.filter(align_id=align_id)
        align_trans_by_grd = [
                align_trans.get(grade_level='12.0').to_json(),
                align_trans.get(grade_level='9.0').to_json(),
                align_trans.get(grade_level='5.0').to_json()]
        trans.extend(align_trans_by_grd)

        q = { 
              'original' : align_trans_by_grd[0]['original'],
              'trans' : align_trans_by_grd }
        questions.append(q)

    # associate each translation with its original 12th grade version
    # before simplification. We need this to include good references.
    for q in questions:
        for t in q['trans']:
            t['original_12th'] = q['original']
            t['type'] = 0

    # log the questions
    log_string = "adequacy-multi questions\n"
    log_string += json.dumps(questions)
    logger.debug(log_string)
    
    # repeats
    repeats = random.sample(questions, NUM_REPEAT)
    questions.extend(repeats)

    # good references
    for t in random.sample(trans, NUM_GOOD_REFS):
        t['type'] = 1
        t['trans_text'] = t['original_12th']

    return HttpResponse(json.dumps(questions))
