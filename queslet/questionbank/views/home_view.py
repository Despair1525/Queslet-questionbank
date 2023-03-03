from django.shortcuts import render
from django.http import HttpRequest
from ..models.models import Mcq
from django.core.paginator import Paginator

# Create your views here.

def home(request):
      
      if request.method == "GET":
        # Load data
    
        result = Mcq.objects.all()
        have_img =Mcq.objects.filter(contain_img =True)
        subjects = Mcq.objects.values('subject').distinct()
        page_num = request.GET.get('page',1)
        p = Paginator(result,10)
        

        page_num = 1 if int(page_num) < 1 else int(page_num)
        page_num = p.num_pages if int(page_num) > p.num_pages else int(page_num)

        page = p.page( page_num)
    
        context ={"lst_mcqs":page,
     "total":len(result),
     "num_img":len(have_img),
     "num_subject":len(subjects),
     "page":page_num
     
     }
        return render(request, 'questionbank.html',context)
