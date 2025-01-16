from django.contrib import admin
from home.models import contactme,user
# Register your models here.

# đăng ký models cho admin site 
admin.site.register(user)
admin.site.register(contactme)
