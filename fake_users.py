import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog_project.settings")
django.setup()
from faker import Faker
from django.contrib.auth.models import User

fake = Faker("ru_RU")


def seed_user(count=10):
    for _ in range(count):
        username = fake.user_name()
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()

        User.objects.create(
            username=username, first_name=first_name, last_name=last_name, email=email
        )


if __name__ == "__main__":
    seed_user()
