from django.shortcuts import render,redirect
from django.http import HttpRequest
from ..models.models import Mcq,Subject,SubjectAccess
from django.core.paginator import Paginator
from django import template
from django.template.defaulttags import register

# Create your views here.

def get_context(request):
    isManager = False

    User =  request.user
    print('current User',User.username)
    isManager = True if  User.groups.filter(name='manager').exists() else False

    result = Mcq.objects.all()

    if not isManager:
        subjects_access = SubjectAccess.objects.filter(teacher=User.   username)
        subjects = [sub.subject for sub in subjects_access]
        if len(subjects) == 0:
            return render(request, 'questionbank.html',{"subjects":subjects,"isManager" :isManager})
        subjects_name = [sub.subject.subject for sub in subjects_access][0]
    else:
        subjects = Subject.objects.all()
        subjects_name = [sub.subject for sub in subjects][0]

        subjects_access_name = [sub.subject for sub in subjects]
        print(subjects_access_name)
        subjects_name_select =  request.GET.get("subject",subjects_name)

        if subjects_name_select in subjects_access_name:
            subjects_name = subjects_name_select
            
        result = result.filter(subject=subjects_name)
        print(subjects)
        have_img = result.filter(contain_img =True)
        page_num = 1
        context ={"lst_mcqs":result,
      "total":len(result),
      "num_img":len(have_img),
      "num_subject":len(subjects),
      "page":page_num,
      "isManager" :isManager,
      "subjects":subjects,
      "subjects_selected":subjects_name
      }
        return context

    


def home(request):
      if not request.user.is_authenticated:
         return redirect('login')
      
      if request.method == "GET":
        # Load data
         #get current user 
        #  isManager = False
        #  if request.user.is_authenticated:
        #     User =  request.user
        #     print('current User',User.username)
        #     isManager = True if  User.groups.filter(name='manager').exists() else False

        #     result = Mcq.objects.all()

        #     if not isManager:
        #        subjects_access = SubjectAccess.objects.filter(teacher=User.   username)
        #        subjects = [sub.subject for sub in subjects_access]
        #        if len(subjects) == 0:
        #            return render(request, 'questionbank.html',{"subjects":subjects,"isManager" :isManager})
        #        subjects_name = [sub.subject.subject for sub in subjects_access][0]
        #     else:
        #        subjects = Subject.objects.all()
        #        subjects_name = [sub.subject for sub in subjects][0]

        #     subjects_access_name = [sub.subject for sub in subjects]
        #     print(subjects_access_name)
        #     subjects_name_select =  request.GET.get("subjected",subjects_name)

        #     if subjects_name_select in subjects_access_name:
        #         subjects_name = subjects_name_select
            
        #     result = result.filter(subject=subjects_name)
        #     print(subjects)

        #     have_img = result.filter(contain_img =True)
        #     page_num = request.GET.get('page',1)
        #     # p = Paginator(result,10)
        #     # page_num = 1 if int(page_num) < 1 else int(page_num)
        #     # page_num = p.num_pages if int(page_num) > p.num_pages else int(page_num)

        #     # page = p.page( page_num)
            context = get_context(request=request)
            return render(request, 'questionbank.html',context)
      else:
          return redirect('login')
      
def isManger(User):
    return User.groups.filter(name='manager').exists() 

@register.filter(name='has_group') 
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists() 