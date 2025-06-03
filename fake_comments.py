import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog_project.settings")
django.setup()
from faker import Faker
from blog.models import Post, Comment
from django.contrib.auth.models import User
from random import choice


fake = Faker("ru_RU")


def seed_comment(count=10):
    for _ in range(count):
        users_count = User.objects.count()
        if users_count > 0:
            author = choice(list(User.objects.all()))
        post_count = Post.objects.count()
        if post_count > 0:
            post = choice(list(Post.objects.all()))
        text = fake.text(max_nb_chars=200)
        Comment.objects.create(post=post, text=text, author=author)


if __name__ == "__main__":
    seed_comment()
