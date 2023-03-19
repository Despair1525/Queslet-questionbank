from django.db import models
from django.contrib.auth.models import  User
# Create your models here.
class Subject(models.Model):
    subject = models.TextField(primary_key=True)
    description = models.TextField(null=True,blank=True)
    user = models.ForeignKey(User, to_field="username",on_delete=models.CASCADE,default="admin")
 
class SubjectAccess(models.Model):
    teacher = models.ForeignKey(User, to_field="username",on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['teacher', 'subject'], name='unique_teacher_subject_combination'
            )
        ]
# 'question','options','answer_q','subject','contain_img','img_file'
class Mcq(models.Model):
    qid = models.CharField(primary_key=True,max_length=100)
    question = models.TextField(null= True, blank= True)
    options = models.CharField(max_length=1000)
    q_image =models.CharField(null= True, blank= True,max_length=500)
    answer_q = models.CharField(null= True, blank= True,max_length=500)
    subject = models.ForeignKey(Subject, to_field="subject",on_delete=models.CASCADE)
    contain_img = models.BooleanField()
    img_file = models.ImageField(null= True, blank= True, upload_to="images/")

    user = models.ForeignKey(User, to_field="username",on_delete=models.CASCADE,default="admin")
 

    
    def getMcq(self,question_image=""): 
        a = 97
        ques = self.question 
        if self.contain_img:
            ques += question_image
        mcq = str(ques) + " "
        ops = self.options[1:-1].split(",")
        for i in range(len(ops)):
            op = ops[i]
            if op.startswith("[") and op.endswith("]"):
                op = op[1:-1]
            mcq += chr(a + i) +")" + " " + str(op) + " "
        return mcq
    
