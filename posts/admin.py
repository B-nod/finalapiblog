from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Friend_Request)
admin.site.register(Post)
admin.site.register(Comment)