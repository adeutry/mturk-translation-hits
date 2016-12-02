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

def get_hit_questions(request):
    '''
    Construct the list of question objects for a single fluency hit
    The list will contain 35 legitimate fluency questions along with
    15 questions for the purpose of quality control
    5 bad references
    5 good references
    5 repeat
    '''
    import nltk

    logger = logging.getLogger("mturk")

    questions = list()

    #pick 40 random translations that can still be used
    all_trans = list(Translation.objects.all().exclude(use_count=0))
    trans = random.sample(all_trans, 40)


    #decrement their use counts
    for t in trans:
        q = { 'original': t.text,
              'trans_text' : t.trans_text,
              'trans_id': t.id ,
              'q_type': '0'}
        questions.append(q)
        t.use_count -= 1
        t.save()

    # log the questions
    log_string = "adequacy questions\n"
    log_string += json.dumps(questions)
    logger.debug(log_string)

    #5 bad references
    # create bad references by randomly removing words
    rmv_count = 2
    bad_trans_orig = random.sample(all_trans, 5)

    for t in bad_trans_orig:
        t_tokens = nltk.word_tokenize(t.trans_text)
        if len(t_tokens) >= rmv_count + 2:
            rand_ind = random.sample(range(1,len(t_tokens)), rmv_count)
            for i in sorted(rand_ind, reverse=True):
                del t_tokens[i]
            trans_text = ' '.join(t_tokens)
            q = { 'trans_text': trans_text,
                  'trans_id': t.id,
                  'q_type': '1',
                  'original' : t.text}
            questions.append(q)
    
    #5 repeats
    repeat_trans = random.sample(trans, 5)
    for t in repeat_trans:
        q = { 'trans_text': t.trans_text,
              'trans_id': t.id,
              'q_type': '3',
              'original': t.text}
        questions.append(q)

    random.shuffle(questions)
    return HttpResponse(json.dumps(questions))
