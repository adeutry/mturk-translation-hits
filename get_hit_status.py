from boto.mturk.connection import MTurkConnection
from boto.mturk.question import ExternalQuestion
from boto.mturk.price import Price
from tabulate import tabulate
import sys
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

AMAZON_HOST = "mechanicalturk.amazonaws.com"
AMAZON_HOST_DEV = "mechanicalturk.sandbox.amazonaws.com"
AMAZON_ACCESS_KEY_ID = config['mturk']['AMAZON_ACCESS_KEY_ID']
AMAZON_SECRET_ACCESS_KEY = config['mturk']['AMAZON_SECRET_ACCESS_KEY']

HIT_URL_PROD = "https://mturk.adeutry.info/fluency_1"
HIT_URL_DEV =  "https://mturk.adeutry.info/fluency_1?dev=True"

# num_hits = 1 or int(iys.argv[1])

if sys.argv[1] == "prod":
    amazon_url = AMAZON_HOST 
    hit_url    = HIT_URL_PROD
elif sys.argv[1] == "dev": 
    amazon_url = AMAZON_HOST_DEV
    hit_url    = HIT_URL_DEV

conn = MTurkConnection(aws_access_key_id=AMAZON_ACCESS_KEY_ID,
                       aws_secret_access_key=AMAZON_SECRET_ACCESS_KEY,
                       host=amazon_url)
hits = list(conn.get_all_hits())

col_names = ['id', 'status', 'review_status', 'available', 'reviewed', 'remaining']
tbl_rows = [col_names]
for hit in [h for h in hits if not h.expired]:
    row = [hit.HITId,
            hit.HITStatus, 
            hit.HITReviewStatus, 
            hit.NumberOfAssignmentsAvailable, 
            hit.NumberOfAssignmentsCompleted, 
            hit.NumberOfAssignmentsPending]
    tbl_rows.append(row)

print(tabulate(tbl_rows))

