from django.contrib import admin
from .models import Post, Comment, LikeComment, LikePost

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(LikeComment)
admin.site.register(LikePost)