import os
import random
import django
import yaml

from django.db import IntegrityError
from faker import Faker

os.environ['DJANGO_SETTINGS_MODULE'] = 'social_network.settings'
django.setup()

from api.models import Post, CustomUser, Reaction

fake = Faker(['en_US'])

config = {}


def parse_config():
    global config
    with open("config.yaml", 'r') as stream:
        config = yaml.safe_load(stream)


def clear_data(users):
    for user in users:
        CustomUser.objects.filter(email=user.email).delete()


def generate_data():
    users = []
    posts = []
    reactions = []
    for _ in range(config['number_of_users']):
        user = CustomUser(email=fake.ascii_email(),
                          password="qwe123")
        users.append(user)
    try:
        CustomUser.objects.bulk_create(users)
        users = CustomUser.objects.filter(email__in=list(map(lambda x: x.email, users)))
        for user in users:
            for _ in range(config['max_posts_per_user']):
                posts.append(Post(user=user,
                                  body=fake.pystr(),
                                  created_at=fake.past_date()))
        Post.objects.bulk_create(posts)
        posts = Post.objects.filter(user__in=users)

        for user in users:
            like_count = 0
            for post in posts:
                if like_count >= config['max_likes_per_user']:
                    break
                if random.random() > 0.3:
                    reactions.append(Reaction(user=user,
                                              post=post,
                                              created_at=fake.date_between(start_date='-2d', end_date='+2d')))
                    like_count += 1
        Reaction.objects.bulk_create(reactions)
        print("Seeded database successfully")
    except (AssertionError, IntegrityError) as e:
        print("Error happened:", e)
        clear_data(users)


if __name__ == '__main__':
    parse_config()
    generate_data()
