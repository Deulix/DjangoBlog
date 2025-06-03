import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog_project.settings")
django.setup()
from faker import Faker
from blog.models import Post
from django.contrib.auth.models import User
from random import choice


fake = Faker("ru_RU")


def seed_post(count=1):
    for _ in range(count):
        users_count = User.objects.count()
        if users_count > 0:
            author = choice(list(User.objects.all()))
        title = fake.text(max_nb_chars=15)
        content = fake.text(max_nb_chars=500)
        Post.objects.create(title=title, content=content, author=author)


if __name__ == "__main__":
    seed_post()
