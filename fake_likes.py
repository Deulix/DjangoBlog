import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog_project.settings")
django.setup()
from faker import Faker
from blog.models import LikePost, LikeComment, Post, Comment
from django.contrib.auth.models import User
from random import choice


fake = Faker("ru_RU")


def seed_like(count=3):
    for _ in range(count):
        users_count = User.objects.count()
        if users_count > 0:
            user = choice(list(User.objects.all()))
        post_count = Post.objects.count()
        if post_count > 0:
            post = choice(list(Post.objects.all()))
        comment_count = Comment.objects.count()
        if comment_count > 0:
            comment = choice(list(Comment.objects.all()))
        if not LikePost.objects.filter(post=post, user=user).exists():
            LikePost.objects.create(post=post, user=user)
        else:
            del LikePost.objects.filter(post=post, user=user)

        if not LikeComment.objects.filter(comment=comment, user=user).exists():
            LikeComment.objects.create(comment=comment, user=user)
        else:
            LikeComment.delete(comment=comment, user=user)


if __name__ == "__main__":
    seed_like()
