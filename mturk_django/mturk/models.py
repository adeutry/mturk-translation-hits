from django.db import models
import pickle

# Create your models here.
class Sentence(models.Model):
    text = models.CharField(max_length=1000)
    slug = models.CharField(max_length=50)
    grade_level = models.CharField(max_length=10)
    align_id = models.IntegerField()

class Translation(models.Model):
    text = models.CharField(max_length=1000)
    slug = models.CharField(max_length=50, default="")
    grade_level = models.CharField(max_length=10, default="")
    align_id = models.IntegerField(default=-1)
    trans_text = models.CharField(max_length=1000)
    trans_lang = models.CharField(max_length=10)
    use_count = models.IntegerField(default=0)
    group = models.IntegerField(default=0)

    def to_json(self):
        '''
        Returns a JSON representation of this objects to be used
        on the client side.
        '''
        q = {
                'original' : self.text,
                'trans_text' : self.trans_text,
                'trans_id' : self.id
                }
        return q

class Paraphrase(models.Model):
    original_text = models.CharField(max_length=1000)
    paraphrase_text = models.CharField(max_length=1000)
    trans_id = models.IntegerField(default=-1)
    username = models.CharField(max_length=1000)

    def to_translation(self):
        '''
        Return the translation representation of this paraphrase object.
        This is used when we are transferring paraphrases into the 
        translations database.
        '''
        from .utils import utils

        # get a translation object with this trans id
        trans_old = Translation.objects.get(pk=self.trans_id)

        # rtt on paraphrase
        para_trans = utils.rtt(self.paraphrase_text, 'de', sleep=0.0)
        
        trans_new = Translation(
                text = self.paraphrase_text,
                slug = trans_old.slug,
                grade_level = trans_old.grade_level,
                align_id = trans_old.align_id,
                trans_text = para_trans,
                trans_lang = 'de',
                use_count = 0,
                group = 3
            )

        return trans_new

def save_sents_to_db():
    with open("/root/python/newsela/data/pickles/aligned_sents_filtered.pick", "rb") as f:
        sents = pickle.load(f)
        for s in sents:
            sent_obj = Sentence(
                text = s['text'],
                slug = s['slug'],
                grade_level = s['grade_level'],
                align_id = s['align_id']
                    )
            sent_obj.save()

def save_trans_to_db():
    with open("/root/python/newsela/data/pickles/aligned_sents_trans.pick", "rb") as f:
        trans = pickle.load(f)
        for t in trans:
            trans_obj = Translation(
               text = t['text'],
               slug = t['slug'],
               grade_level = t['grade_level'], 
               align_id = t['align_id'],
               trans_text = t['trans-text'],
               trans_lang = t['trans-lang'],
               use_count = 0
            )
            trans_obj.save()
