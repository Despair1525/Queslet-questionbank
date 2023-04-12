from django.shortcuts import render,redirect
from django.http import HttpResponse

from .home_view import home
from ..models.models import Mcq
from..forms import McqForm
from ..Dbcontext import connector
conn = connector()
def edit_mcq(request):


    if request.method == 'POST':

        mcq_id = request.POST.get('qid')
        form = McqForm(request.POST)
        print(form.errors)
        print(request.POST)

        if form.is_valid():
            print("form is valid")

            try:
                mcq = Mcq.objects.get(qid=mcq_id)
            except:
                return redirect('forbiden')
            # Update and save data

            # if remove buttons 
            if  request.POST.get('remove') is not None:
                
                # remove database 
                # remove vectors 
                ids =[str(mcq.qid )]
                subject = str(mcq.subject )
                print("Delete",(ids,subject))
                try:
                    print( conn.remove_index(ids,subject) )
                    print(str(mcq),"delete successfull !")
                    mcq.delete()
                except:
                    print("Delete fails !")
                return redirect('home')

            answer_Q = request.POST.get('answer_q')
            mcq.question = request.POST.get('question')
            mcq.options = request.POST.get('options')
            mcq.contain_img = True if request.POST.get('contain_img') is not None else False

            if mcq.contain_img:
                clear_img = True if request.POST.get('img_file-clear') is not None else False
                print(clear_img)
                new_image = request.FILES.get('img_file')
                if clear_img:
                    mcq.img_file.delete(save=False)
                if new_image is not None:
                    print(" change FILE Image",new_image)
                    img_name = str(new_image)
                    mcq.q_image = img_name
                    mcq.img_file = new_image

                #get file image 
            mcq.answer_q= answer_Q

            mcq.save()
            form = McqForm(instance=mcq)
            response = redirect('mcq_view')
            agrs = '?mcq='+ str(mcq_id)
            response['Location'] += agrs

            return response

        else:
            print("Form not vald ")
    
    else:
    #get MCQ
        mcq_id = request.GET.get('mcq')
        try:
            mcq = Mcq.objects.get(qid=mcq_id)
        except:
            return redirect('forbiden')
        print(mcq.question)
        form = McqForm(instance=mcq)
    

    return render(request, 'edit_mcq.html',{"form":form,"mcq_id":mcq_id})
