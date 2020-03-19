from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from .models import Question,Choice
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.


#normal way of writing views //

# def index(request):
#     question =Question.objects.all()[:]
#     context = {
#         'question':question,
#     }
#     return render(request,'polls/index.html',context)

# def details(request,id):
#     # question=Question.objects.get(pk=id)
#     question=get_object_or_404(Question,pk=id)
#     context ={
#         'question':question,
#     }
#     return render(request,'polls/details.html',context)

# def results(request,id):
#     question=Question.objects.get(pk=id)
#     # choice=Choice.objects.all()
#     context={
#         # 'choice':choice,
#         'question':question,
#     }
#     return render(request,'polls/results.html',context)


#
# using generic views we can reuse code i.e.  can use for basic operations such as fetching data from database..

class IndexView(generic.ListView):
    template_name='polls/index.html'
    context_object_name='question'
    def get_queryset(self):
        q=Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
        return q 

class DetailsView(generic.DetailView):
    template_name='polls/details.html'
    model=Question
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultView(generic.DetailView):
    template_name='polls/results.html'
    model=Question


@login_required
def vote(request,id):
    question=get_object_or_404(Question,pk=id)
    try:
        choice=question.choice_set.get(pk=request.POST['choice'])

    except(KeyError,Choice.DoesNotExist):
        return render(request,'polls/details.html',{
            'question':question,
            'error_message':'you didnt choose a option',
        })
    else:
        choice.votes+=1
        choice.save()
        return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))

    

