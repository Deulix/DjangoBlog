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

        like_post = LikePost.objects.filter(user=user, post=post)
        if like_post:
            like_post.delete()
        else:
            LikePost.objects.create(user=user, post=post)

        like_comment = LikeComment.objects.filter(user=user, comment=comment)
        if like_comment:
            like_comment.delete()
        else:
            LikeComment.objects.create(user=user, comment=comment)
            


if __name__ == "__main__":
    seed_like()
