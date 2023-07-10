from .models import BaseUser, Profile, Post, Subscription
from django.db import transaction
from django.db.models import QuerySet
from django.utils.text import slugify
from django.core.cache import cache


def create_profile(*, user: BaseUser, bio: str | None) -> Profile:
    return Profile.objects.create(user=user, bio=bio)


def create_user(*, email: str, password: str) -> BaseUser:
    return BaseUser.objects.create_user(email=email, password=password)


@transaction.atomic
def register(*, bio: str | None, email: str, password: str) -> BaseUser:
    user = create_user(email=email, password=password)
    create_profile(user=user, bio=bio)

    return user


def count_follower(*, user: BaseUser) -> int:
    return Subscription.objects.filter(target=user).count()


def count_following(*, user: BaseUser) -> int:
    return Subscription.objects.filter(subscriber=user).count()


def count_posts(*, user: BaseUser) -> int:
    return Post.objects.filter(author=user).count()


def cache_profile(*, user: BaseUser) -> None:
    profile = {
        "posts_count": count_posts(user=user),
        "subscribers_count": count_follower(user=user),
        "subscriptions_count": count_following(user=user),
    }
    cache.set(f"profile_{user}", profile, timeout=None)


@transaction.atomic
def create_post(*, user: BaseUser, title: str, content: str) -> QuerySet[Post]:
    post = Post.objects.create(
        author=user, title=title, content=content, slug=slugify(title)
    )

    cache_profile(user=user)
    return post


def subscribe(*, user: BaseUser, email: str) -> QuerySet[Subscription]:
    target = BaseUser.objects.get(email=email)
    sub = Subscription(subscriber=user, target=target)
    sub.full_clean()
    sub.save()
    cache_profile(user=user)
    return sub


def unsubscribe(*, user: BaseUser, email: str) -> dict:
    target = BaseUser.objects.get(email=email)
    Subscription.objects.get(subscriber=user, target=target).delete()
    cache_profile(user=user)


def profile_count_update():
    profiles = cache.keys("profile_*")

    for profile_key in profiles: 
        email = profile_key.replace("profile_", "")
        data = cache.get(profile_key)

        try:
            profile = Profile.objects.get(user__email=email)
            profile.posts_count = data.get("posts_count")
            profile.subscribers_count = data.get("subscribers_count")
            profile.subscriptions_count = data.get("subscriptions_count")
            profile.save()

        except Exception as ex:
            print(ex)