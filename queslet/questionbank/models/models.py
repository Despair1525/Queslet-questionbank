from django.db import models

# Create your models here.
class Mcq(models.Model):
    qid = models.TextField(primary_key=True)
    question = models.TextField(null= True, blank= True)
    options = models.TextField()
    q_image =models.TextField(null= True, blank= True)
    answer_q = models.TextField(null= True, blank= True)
    subject = models.TextField()
    contain_img = models.BooleanField()

    img_file = models.ImageField(null= True, blank= True, upload_to="images/")

    
 
    class Meta:
        db_table = "mcqs"