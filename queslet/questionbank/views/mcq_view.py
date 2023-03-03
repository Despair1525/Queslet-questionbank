from django.shortcuts import render
from django.http import HttpResponse

from .home_view import home
from ..models.models import Mcq

def mcq_view(request):
    if request.method == "GET":
        
        mcq_id = request.GET.get("mcq")
        if mcq_id == None:
            return home(request)
        
        result = Mcq.objects.all()
        mcqs =  result.filter(qid = str(mcq_id.strip()))
        temp_path = 0

        if request.GET.get("temp") != None and len(mcqs) == 0 :
            dct_mcq = request.session['temp_mcq']
            mcq = dct_mcq[str(mcq_id.strip())]
            id = mcq['id']
            question = mcq["question"]
            image = mcq["image"]
            options = mcq["options"]
            answer = mcq["answer"]
            subject = mcq["subject"]
            haveImage = mcq["haveImage"]
            temp_path = 1
            # qid = models.TextField(primary_key=True)
#     question = models.TextField()
#     options = models.TextField()
#     q_image =models.TextField()
#     answer_q = models.TextField()
#     subject = models.TextField()
#     contain_img = models.BooleanField()

            mcqs =[ {"qid": id, "question":question, "options":options, "q_image":image,"answer_q":answer, "subject" :subject, "contain_img" : haveImage  } ]

            print(mcqs)
        return render(request, 'mcq.html',{"mcqs":mcqs,"temp_path":temp_path})