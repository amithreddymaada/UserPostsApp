from django.test import TestCase



# Create your tests here.
from django.utils import timezone
import datetime
from polls.models import Question
from django.urls import reverse

class QuestionModelTests(TestCase):

    def test_was_recently_published_future_question(self):
        time=timezone.now() + datetime.timedelta(days=30)
        future=Question(pub_date=time)
        self.assertIs(future.was_recently_published(),False)

    def test_was_recently_published_recent_question(self):
        time=timezone.now() - datetime.timedelta(hours=23,minutes=59,seconds=59)
        recent=Question(pub_date=time)
        self.assertIs(recent.was_recently_published(),True)

    def test_was_recently_published_older_question(self):
        time=timezone.now() - datetime.timedelta(days=1,seconds=1)
        older=Question(pub_date=time)
        self.assertIs(older.was_recently_published(),False)
    
def create_question(question_text,days):
    time=timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text,pub_date=time)

class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        response=self.client.get(reverse('polls:index'))
        # response=self.client.get('localhost:8000/polls/')
        self.assertEqual(response.status_code,200)
        self.assertContains(response,'No polls are available')
        self.assertQuerysetEqual(response.context['question'],[])
    
    def test_past_questions(self):
        question=create_question("past question",-30)
        response=self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code,200)
        self.assertQuerysetEqual(response.context['question'],['<Question: past question>'])
    
    def test_future_questions(self):
        question=create_question("future question",30)
        response=self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,'No polls are available')
        self.assertQuerysetEqual(response.context['question'],[])

    def test_future_question_and_past_question(self):
        future_question=create_question("future question",30)
        past_question=create_question("past question",-30)
        response=self.client.get(reverse('polls:index'))
        self.assertIs(response.status_code,200)
        self.assertQuerysetEqual(response.context['question'],['<Question: past question>'])
    def test_two_past_questions(self):
        past_1=create_question("past question1",-30)
        past_2=create_question("past question2",-30)
        response=self.client.get(reverse('polls:index'))
        self.assertIs(response.status_code,200)
        self.assertQuerysetEqual(response.context['question'],['<Question: past question2>','<Question: past question1>'])

class QuestionDetailsViewTests(TestCase):

    def test_future_question(self):
        future_question=create_question('future question',5)
        response=self.client.get(reverse('polls:details',args=(future_question.id,)))
        self.assertEqual(response.status_code,404)
        
    def test_past_question(self):
        past_question=create_question("past question",-5)
        response=self.client.get(reverse('polls:details',args=(past_question.id,)))
        self.assertContains(response,past_question.question_text)
    
    