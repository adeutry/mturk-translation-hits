import requests, time, csv, nltk, codecs, re
from operator import itemgetter
import pdb


def google_translate(string, source, target):
    key = "AIzaSyAGVLVH448yV8bKExR_c3s1CeOHTXLB1BQ"
    url = ("https://www.googleapis.com/language/translate/v2?key=" + key + 
        "&source=" + source + 
        "&target=" + target + 
        "&q=" + string)
    res = requests.get(url)
    return res.json()['data']['translations'][0]['translatedText']

def round_trip_translate(string, target, sleep=1.0):
    translated = google_translate(string, "en", target)
    translated = translated.replace("&quot;",'"')
    time.sleep(sleep)
    original = google_translate(translated, target, "en")
    time.sleep(sleep)
    return original.replace("&quot;", '"').replace("&#39","'")

def rtt(string, target, sleep=1.0):
    return round_trip_translate(string, target, sleep)
