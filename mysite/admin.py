from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(NewsInfo)
admin.site.register(D2NewsInfo)
admin.site.register(Comment)
