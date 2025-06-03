from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_liked_by(self, user):
        return self.likes.filter(user=user).exists()

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey('Comment', null=True, blank=True, on_delete=models.CASCADE)

    def is_liked_by(self, user):
        return self.likes.filter(user=user).exists()
    
    def __str__(self):
        return f"Комментарий пользователя {self.author} в {self.post.title}"
    
class LikePost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['post', 'user']
        verbose_name = 'Лайк поста'
        verbose_name_plural = 'Лайки постов'

    def __str__(self):
        return f'Пользователь {self.user} поставил лайк на {self.post}'

class LikeComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_comment')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['comment', 'user']
        verbose_name = 'Лайк комментария'
        verbose_name_plural = 'Лайки комментариев'

    def __str__(self):
        return f'Пользователь {self.user} поставил лайк на {self.comment}'




