from boto.mturk.connection import MTurkConnection
from boto.mturk.question import ExternalQuestion
from boto.mturk.price import Price
from tabulate import tabulate
import sys, json, django

# setup django so it actually works
django.setup()

# amazon authentication
AMAZON_HOST = "mechanicalturk.amazonaws.com"
AMAZON_HOST_DEV = "mechanicalturk.sandbox.amazonaws.com"
AMAZON_ACCESS_KEY_ID = "AKIAJYJ3K46RLMO6KA5Q"
AMAZON_SECRET_ACCESS_KEY = "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"

if sys.argv[1] == "prod":
    amazon_url = AMAZON_HOST 
elif sys.argv[1] == "dev": 
    amazon_url = AMAZON_HOST_DEV

conn = MTurkConnection(aws_access_key_id=AMAZON_ACCESS_KEY_ID,
                       aws_secret_access_key=AMAZON_SECRET_ACCESS_KEY,
                       host=amazon_url)
# load the hits
hits = list(conn.get_all_hits())
assignments = list()
results = list()
all_answers = list()
ratings = list()

# load the assignments for each hit
for hit in [h for h in hits if not h.expired]:
    hit_assigns = conn.get_assignments(hit.HITId)
    assignments.extend(hit_assigns)

# make list of results. Each element is the result of one HIT
for assign in assignments:
    answers = {ans.qid:ans.fields[0] for ans in assign.answers[0]}
    all_answers.append(answers)
    res = {
        'workerId' : answers['workerId'],
        'answerData' : json.loads(answers['answerData']),
        'totalTime' : answers['totalHitTime']
        }
    results.append(res)

# make the list of ratings. 3 for each result
for res in results:
    for ans in res['answerData'][0]['trans']:
        rating = {
            'totalTime' : res['totalTime'],
            'workerId' : res['workerId'],
            'answer' : ans['answer'],
            'type' : ans['type'],
            'transId' : ans['trans_id']
            }
        ratings.append(rating)

from mturk.models import Translation

trans_all = Translation.objects.all()
for r in ratings:
    trans = trans_all.get(id=r['transId'])
    r.update(trans.__dict__)
