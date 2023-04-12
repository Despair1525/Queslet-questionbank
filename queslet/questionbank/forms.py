
from django import forms
from django.forms import ModelForm
from .models.models import Mcq
class UploadFileForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple':True,'accept':'image/*,.doc, .docx'}))

class McqForm(ModelForm):
    class Meta:
        model = Mcq
        fields = ('question','options','answer_q','contain_img','img_file') 
        # fields = '__all__'

        widgets ={
            # 'qid':forms.TextInput(attrs={'readonly':True,'class':'read-only'}),
            'q_image':forms.TextInput(attrs={'readonly':True,'class':'read-only'}),
'question':forms.Textarea(attrs={'class':'text-box','cols':80 ,'rows':10}),
'options':forms.TextInput(attrs={'class':'text-box'}),
'answer_q':forms.TextInput(attrs={'class':'text-box'})
        }


