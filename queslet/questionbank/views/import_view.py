


#Upload File
from ..forms import UploadFileForm
from django.core.files.storage import default_storage
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from ..models.models import Mcq
from docx import Document
import os
import shutil
import time
import re
import easyocr
from PIL import Image

import torch
from sentence_transformers import SentenceTransformer
from ..Dbcontext import connector
from.home_view import home
#regex find image_path 
img_regex = "(?<=\[file: ).+?(?=\])"
ques_regex = "(\[file:).*?(\])"
op_regex = "([a-zA-Z]\.)"

#Easy OCR 
reader = easyocr.Reader(['en','vi'])

print("Connecting to pinecone")
conn = connector()

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print("Device:",device)
print("Loading SBert Model ")
SbertModel = SentenceTransformer('model\\all-mpnet-finetune-5epochs',device=device)

#Sbert 

def import_view(request):
    if request.method == "POST":

        if 'submit_import' in request.POST:
            checked_items = request.POST.getlist("check_import")
            #show import mcq
            print(checked_items)
            print("--------------------------")
            temp_dct = request.session['temp_mcq']


            for key_mcq in checked_items:
                mcq = temp_dct[key_mcq]
                print( mcq )
                print(mcq["encode"])
                subject = mcq["subject"]
                #generate new id
                user_name ="admin"
                new_id = subject+"-"+user_name+"-"+get_time()
                #get attr
                question = mcq["question"]
                options = mcq["options"]
                answer = mcq["answer"]
                haveImage = mcq["haveImage"]

                if haveImage:
                    images = new_id+".png"
                    temp_path = "media/temp/"+mcq["image"]
                    image_path = "media/images/"+images
                    new_path = "images/"+images
                    shutil.move(temp_path, image_path)

                    save_mcq= Mcq( 
                        qid =  new_id,
                        question = question,
                        options = options,
                        q_image = images,
                        answer_q = answer,
                        subject = subject,
                        contain_img = haveImage,
                        img_file = new_path )
                    # save_mcq.save()
                else:
                    save_mcq= Mcq( 
                        qid =  new_id,
                        question = question,
                        options = options,
                        answer_q = answer,
                        subject = subject,
                        contain_img = haveImage
                         )
                    # save_mcq.save()
                
    #                 qid = models.TextField(primary_key=True)
    # question = models.TextField(null= True, blank= True)
    # options = models.TextField()
    # q_image =models.TextField(null= True, blank= True)
    # answer_q = models.TextField(null= True, blank= True)
    # subject = models.TextField()
    # contain_img = models.BooleanField()

    # img_file = models.ImageField(null= True, blank= True, upload_to="images/")

                break
            
            
            return redirect(home)
        else:
            form = UploadFileForm(request.POST,request.FILES)
            files = request.FILES.getlist('file')
            list_docx={}
            list_images={} 

            #Load Images and docx file 
            for file in files:
                name_file,ex = os.path.splitext(str(file))
                # document = Document(file)
                if ex in ['.docx']:
                    print("found document")
                    list_docx[str(file)] = []
                    doc = Document(file)
                    for table in doc.tables:
                        new_mcq = row2mcq(table)
                        list_docx[str(file)].append(new_mcq)
                    # print("Total questions:",len(doc.tables))
                else:
                    list_images[str(file)] = file

                    save_path = "temp/"+file.name
                    default_storage.save(save_path, file)
                    
                    #reading Url 
                    # file_url = default_storage.url(save_path)

                    # print("Image_path:",file_url)
            duplicate_mcq =[]
            mcqs_set={}
            for key in list_docx.keys():
                for mcq in list_docx[key]:
                    #store in session 
                   
                    print(mcq.qid)
                    mcq_image_text =""
                    
                    if mcq.contain_img:
                        file_img = list_images[mcq.q_image]
                        mcq_image_text = ocr2Text(file_img)
                    mcq_form = mcq.getMcq(mcq_image_text)

                        # print(mcq_form)
                    encode = SbertModel.encode(str(mcq_form)).tolist()
                    result = conn.query_mcqs_encode(encode,str(mcq.subject).strip(),k=5)

                        # Filter dictionary by keeping elements whose keys are divisible by 2
                    list_id_dup = [ (d["id"],d["score"]) for d in result["matches"] if d["score"] >= 0.75] 
                    if len(list_id_dup) ==0:
                        continue
                    duplicate_mcq.append((mcq,list_id_dup))

                    mcqs_set[mcq.qid] = {"id":mcq.qid,"question":mcq.question,"image":mcq.q_image,"options":mcq.options,"answer":mcq.answer_q,"subject":mcq.subject,"haveImage":mcq.contain_img,"encode":encode} 

            # print("total images",len(list_images))
            # print(list_images)
            request.session['temp_mcq'] = mcqs_set
            # test_dct = request.session['temp_mcq']
            # print(test_dct)
            # print(mcqs_set)
            return render(request, 'import.html',{'dup_result':duplicate_mcq})
    else:
        form = UploadFileForm()
    return render(request, 'import.html',{'form':form})




def ocr2Text(file):
    path="temp.png"
    img = Image.open(file)
    img.save(path)
    img_text = reader.readtext(path, paragraph=True)

    question = ""
    for i in img_text:
        question += i[1] +" "
    return question

def get_time():
    t = time.time()
    t_s = int(t)
    return str(t_s)

def row2mcq(table,subject="math"):
    data = [[cell.text for cell in row.cells] for row in table.rows]
    mcq_options = []
    ans =""
    for row in data:
        if(row[0].strip() == "answer"):
            ans = row[1]
        if("QN" in row[0]):
            mcq_name = row[0]
            text = row[1]
            text = text.replace("\n"," ")
            path = re.findall(img_regex,text) 
            if(len(path) == 0 ):
                path =""
            else:
                path = path[0]                
            question = re.sub(ques_regex, '',text )
            mcq_question = question
            # print("Question:",question)
            mcq_images = path
       
        if(re.match(op_regex,row[0])):
            text = row[1]
            text = text.replace("\n"," ")
            if len(text.strip()) != 0 :
                mcq_options.append(text)
    # print(mcq_images)
    # print(mcq_options)
    contain_img = False if len(mcq_images.strip()) <=0 else True
    if contain_img:
        new_mcq = Mcq(qid = mcq_name,question = mcq_question,options = str(mcq_options) , q_image = mcq_images , answer_q = ans, subject = subject, contain_img = contain_img, img_file = "temp/"+  mcq_images )
    else:
        new_mcq = Mcq(qid = mcq_name,question = mcq_question,options = str(mcq_options) , q_image = mcq_images , answer_q = ans, subject = subject, contain_img = contain_img )

    # new_mcq = mcq(mcq_name,mcq_question,mcq_options,"",images=mcq_images,haveImages=contain_img, subject="math")
    return new_mcq

    # qid = models.TextField(primary_key=True)
    # question = models.TextField(null= True, blank= True)
    # options = models.TextField()
    # q_image =models.TextField(null= True, blank= True)
    # answer_q = models.TextField(null= True, blank= True)
    # subject = models.TextField()
    # contain_img = models.BooleanField()

    # img_file = models.ImageField(null= True, blank= True, upload_to="images/")