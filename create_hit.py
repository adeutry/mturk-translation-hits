from boto.mturk.connection import MTurkConnection
from boto.mturk.question import ExternalQuestion
from boto.mturk.price import Price
import sys

AMAZON_HOST = "mechanicalturk.amazonaws.com"
AMAZON_HOST_DEV = "mechanicalturk.sandbox.amazonaws.com"
AMAZON_ACCESS_KEY_ID = "AKIAJYJ3K46RLMO6KA5Q"
AMAZON_SECRET_ACCESS_KEY = "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"

conn = MTurkConnection(aws_access_key_id=AMAZON_ACCESS_KEY_ID,
                       aws_secret_access_key=AMAZON_SECRET_ACCESS_KEY,
                       host=AMAZON_HOST)

HIT_URL_PROD = "https://mturk.adeutry.info/fluency_1"
HIT_URL_DEV =  "https://mturk.adeutry.info/fluency_1?dev=True"

title = "Evaluate Translations"
description = "Evaluate the performance of Machine Translation systems. Judge how fluent a sentence is."
keywords = ["language", "translation"]
frame_height = 650
amount = 0.30

question_form = ExternalQuestion(url, frame_height)

# num_hits = 1 or int(iys.argv[1])

if sys.argv[1] == "prod":
    amazon_url = AMAZON_HOST 
    hit_url    = HIT_URL_PROD
else if sys.argv[1] == "dev": 
    amazon_url = AMAZON_HOST_DEV
    hit_url    = HIT_URL_DEV

for i in range(1):
        create_hit_result = conn.create_hit(
                title = title,
                description = description,
                keywords = keywords,
                max_assignments = 5,
                question = question_form,
                reward = Price(amount=amount)
                )
