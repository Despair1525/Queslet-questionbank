from django.contrib import admin

# Register your models here.
from .models.models import Mcq,Subject,SubjectAccess
admin.site.register(Subject)

admin.site.register(Mcq)

admin.site.register(SubjectAccess)

