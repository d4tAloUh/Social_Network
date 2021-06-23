from django.contrib import admin
from .models import CustomUser, Reaction, Post

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Reaction)
admin.site.register(Post)
