from django.contrib import admin
from blogapp.models import *
# Register your models here.
admin.site.register(blog)
admin.site.register(trending_topics)
admin.site.register(likes)
admin.site.register(User)
admin.site.register(comment)





