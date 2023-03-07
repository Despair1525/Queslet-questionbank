from django.shortcuts import render,redirect
from django.http import HttpRequest
from ..models.models import Mcq,SubjectAccess,Subject
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from ..ultils import isManger
from django.core.paginator import Paginator
from django.contrib import messages

# Create your views here.

def manage(request):

    context = get_grouped()

    
    if(request.method == "POST"):

        teacherLst = context["teacherList"]
        subjectLst = context["subjectLst"]

        for teacher in teacherLst:
            for subject in subjectLst:

                check_name = teacher+"-"+subject
                
                checked = False if request.POST.get(check_name) is None else True
                checkAccess(teacher,subject,checked)
        messages.success(request,("Save successfully !"))
        return redirect('manage')
                # check tick box
                # if checked is None:
                    
                





    return render(request, 'manage.html',context)


def checkAccess(teacherName,subjectname,checked):
    User = get_user_model()
    teacher = User.objects.get(username=teacherName)
    subject = Subject.objects.get(subject = subjectname)
    try:
        sb = SubjectAccess.objects.get(teacher = teacher,subject= subject)
    except:
        print("Not found")
        sb = None
    
    if sb is None and checked:
        print("Create new Access !")
        newAccess = SubjectAccess.objects.create(teacher=teacher,subject=subject)
        newAccess.save()
    elif sb is not None and not checked:
        print("Remove access of:",teacherName,"in",subjectname)
        sb.delete()

        

def get_grouped():
    grouped = dict()

    for obj in SubjectAccess.objects.all():
        if not isManger(obj.teacher):
            grouped.setdefault(obj.teacher.username, []).append(obj.subject.subject)
    User = get_user_model()
    teacherLst = [user.username for user in User.objects.all() if not isManger(user)]
  
    subjectLst = [sub.subject for sub in Subject.objects.all() ]
    print(grouped)
  

    context = {"teacherList":teacherLst,"subjectLst":subjectLst,"access":grouped}
    return context