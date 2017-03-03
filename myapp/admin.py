from django.contrib import admin
from myapp.models import *
# Register your models here.
admin.site.register(Member)
admin.site.register(Department)
admin.site.register(Record)
admin.site.register(AdminObject)
admin.site.register(UserObject)
