from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.StudentDetails)
admin.site.register(models.TeacherDetails)

admin.site.register(models.Finals)
admin.site.register(models.Term1)
admin.site.register(models.Term2)
