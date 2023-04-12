from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from sentence_transformers import SentenceTransformer
import torch

# load Sbert model 
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print("Device:",device)
print("Loading SBert Model ")
SbertModel = SentenceTransformer('model\\all-mpnet-finetune-5epochs',device=device)

@api_view(['GET', 'POST'])
def model_encode(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        mcq = request.GET.get('mcq')
        encode = SbertModel.encode(mcq).tolist()

        return Response({"encode": encode})

    # elif request.method == 'POST':
    #     serializer = SnippetSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response("errors", status=status.HTTP_400_BAD_REQUEST)