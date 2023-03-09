from django.contrib import admin

# Register your models here.
from .models.models import Mcq,Subject,SubjectAccess
admin.site.register(Subject)

admin.site.register(Mcq)

admin.site.register(SubjectAccess)

admin.site.site_header = "Queslet administration"
admin.site.site_title = "Queslet administration"
admin.site.index_title = "Queslet administration"
# admin.site.