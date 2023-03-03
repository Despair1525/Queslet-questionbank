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
    
    class Meta:
        db_table = "mcqs"