from boto.mturk.connection import MTurkConnection
from boto.mturk.question import ExternalQuestion
from boto.mturk.price import Price
import sys

AMAZON_HOST = "mechanicalturk.amazonaws.com"
AMAZON_HOST_DEV = "mechanicalturk.sandbox.amazonaws.com"
AMAZON_ACCESS_KEY_ID = "AKIAJYJ3K46RLMO6KA5Q"
AMAZON_SECRET_ACCESS_KEY = "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"

hit_infos = {
    'fluency' : {
            'title' : 'Evaluate Translation Fluency',
            'description' : 'Evaluate how fluently a Machine translation is composed.',
            'keywords' : ["language", "translation"],
            'frame_height' : 650,
            'amount' : 0.35,
            'prod_url' :  "https://mturk.adeutry.info/fluency_1",
            'dev_url' : "https://mturk.adeutry.info/fluency_1?dev=True"
    },
    'adequacy' : {
            'title' : 'Evaluate Translation Adequacy',
            'description' : 'Evaluate how adequate a translation is compared to the original.',
            'keywords' : ["language", "translation"],
            'frame_height' : 650,
            'amount' : 0.50,
            'prod_url' : "https://mturk.adeutry.info/adequacy_1",
            'dev_url' : "https://mturk.adeutry.info/adequacy_1?dev=True"
    },
    'adequacy_multi' : {
            'title' : 'Evaluate Translation Adequacy',
            'description' : 'Evaluate how adequate a translation is compared to the original.',
            'keywords' : ["language", "translation"],
            'frame_height' : 1500,
            'amount' : 0.03,
            'prod_url' : "https://mturk.adeutry.info/adequacy_multi",
            'dev_url' : "https://mturk.adeutry.info/adequacy_multi?dev=True"
    }
}

hit_type = sys.argv[1]
env = sys.argv[2]

hit_info = hit_infos[hit_type]

if env == "prod":
    amazon_url = AMAZON_HOST 
    hit_url = hit_info['prod_url']
elif env == "dev": 
    amazon_url = AMAZON_HOST_DEV
    hit_url = hit_info['dev_url']

question_form = ExternalQuestion(hit_url, hit_info['frame_height'])

conn = MTurkConnection(aws_access_key_id=AMAZON_ACCESS_KEY_ID,
                       aws_secret_access_key=AMAZON_SECRET_ACCESS_KEY,
                       host=amazon_url)

for i in range(20):
        create_hit_result = conn.create_hit(
                title = hit_info['title'],
                description = hit_info['description'],
                keywords = hit_info['keywords'],
                max_assignments = 25,
                question = question_form,
                reward = Price(amount=hit_info['amount'])
                )
