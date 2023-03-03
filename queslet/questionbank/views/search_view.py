
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ..models.models import Mcq
#MC model 

#MC model 
import torch
from sentence_transformers import SentenceTransformer

from ..Dbcontext import connector

#load Sbert model 
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print("Device:",device)
print("Loading SBert Model ")
SbertModel = SentenceTransformer('model\\all-mpnet-finetune-5epochs',device=device)

# connect to pinecone
print("Connecting to pinecone")
conn = connector()


@csrf_exempt 
def search_view(request):

    if request.method =="GET":
        if request.GET.get("search_text") != None:
            search_text = request.GET.get("search_text")
            encode_search = SbertModel.encode(str(search_text)).tolist()
            search_result = conn.query_mcqs_encode(encode_search,"math",k=10)

            print(search_result)
            #get List mcqs 
            list_id = [d["id"] for d in search_result["matches"] if d["score"] >= 0.23] 

            result_found =  Mcq.objects.filter(pk__in= list_id)
    context={"lst_mcqs":result_found} 
    return render(request, 'questionbank_search.html',context)