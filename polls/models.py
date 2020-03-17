from django.db import models
import datetime
from django.utils import timezone

# Create your models here.

class Question(models.Model):
    question_text=models.CharField(max_length=200)
    pub_date=models.DateTimeField('date published')

    def __str__(self):
        return self.question_text
    def was_recently_published(self):
        time=timezone.now() - datetime.timedelta(days=1)
        return self.pub_date >= time and self.pub_date <=timezone.now() 
    was_recently_published.short_description='Published recently'
    was_recently_published.boolean=True

class Choice(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes=models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
