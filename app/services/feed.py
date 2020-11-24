from itertools import chain
from random import randint

from app.exceptions import InvalidInputFormat
from app.models.account import Account
from app.models.company import Company
from app.models.job import Job
from app.models.post import Post
from app.models.user import User
from app.models.comment import Comment
from app.models.follow import Follow


def get_feed(*, account: Account, t: int, q: int) -> list:
    # user = get_user_account(account)

    f = Follow.objects.filter(sender=account, receiver__account_type='company')
    followed_companies = [get_company_account(c.receiver) for c in f]
    # Company.objects.filter(followers=user)
    job_list = Job.objects.filter(
        company__in=followed_companies,
        published_date__lt=t).order_by('-published_date')

    # followed_users = User.objects.filter(followers=user)
    f = Follow.objects.filter(sender=account, receiver__account_type='user')
    followed_users = [get_user_account(c.receiver) for c in f]
    post_list = Post.objects.filter(
        user__in=followed_users,
        published_date__lt=t).order_by('-published_date')

    feed = list(sorted(chain(job_list, post_list),
                       key=lambda instance: instance.published_date,
                       reverse=True))
    feed = list(dict.fromkeys(feed))
    return feed[:q]


def suggest_follow(*, account: Account) -> list:
    NUMBER_OF_SUGGESTION = 3
    user = get_user_account(account)

    comps = Company.objects.exclude(followers=user)
    if comps.count() < NUMBER_OF_SUGGESTION:
        suggest_companies = comps
    else:
        fst = randint(0, comps.count() - NUMBER_OF_SUGGESTION)
        suggest_companies = comps[fst:fst + NUMBER_OF_SUGGESTION]

    users = User.objects.exclude(followers=user)
    if users.count() < NUMBER_OF_SUGGESTION:
        suggest_users = users
    else:
        fst = randint(0, users.count() - NUMBER_OF_SUGGESTION)
        suggest_users = user[fst:fst + NUMBER_OF_SUGGESTION]

    suggest = list(sorted(chain(suggest_users, suggest_companies),
                          key=lambda instance: instance.account.id))
    suggest = list(dict.fromkeys(suggest))
    return suggest


def count_comment(id: int) -> int:
    return Comment.objects.filter(post__id=id).count()


def get_company_account(account: Account) -> Company:
    c = Company.objects.filter(account=account).first()
    if c is None:
        raise InvalidInputFormat("Company not found!")
    return c


def get_user_account(account: Account) -> User:
    e = User.objects.filter(account=account).first()
    if e is None:
        raise InvalidInputFormat("User not found!")
    return e
