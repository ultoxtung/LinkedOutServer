from itertools import chain
from random import randint

from app.exceptions import InvalidInputFormat
from app.models.account import Account
from app.models.company import Company
from app.models.job import Job
from app.models.post import Post
from app.models.skill import Skill
from app.models.user import User


def get_feed(*, account: Account) -> list:
    user = get_user_account(account)

    followed_companies = Company.objects.filter(followers=user)
    job_list = Job.objects.filter(
        company__in=followed_companies).order_by('-published_date')

    already_have_skills = user.skills.all()
    sid = []
    [sid.append(s.id) for s in already_have_skills]
    not_have_skills = Skill.objects.exclude(id__in=sid)
    post_list = Post.objects.all().order_by('-published_date')

    feed = list(sorted(chain(job_list, post_list),
                       key=lambda instance: instance.published_date, reverse=True))
    feed = list(dict.fromkeys(feed))
    return feed


def suggest_job(*, account: Account) -> list:
    NUMBER_OF_SUGGESTION = 3
    user = get_user_account(account)

    already_have_skills = user.skills.all()
    sid = []
    [sid.append(s.id) for s in already_have_skills]
    not_have_skills = Skill.objects.exclude(id__in=sid)
    job_list = Job.objects.filter(
        skills__in=already_have_skills).order_by('-published_date')
    job_list = job_list.exclude(
        skills__in=not_have_skills).order_by('-published_date')
    job_list = job_list.exclude(
        company__followers=user).order_by('-published_date')

    res = list(job_list)
    res = list(dict.fromkeys(res))

    if len(res) < NUMBER_OF_SUGGESTION:
        return res
    first_post = randint(0, len(res) - NUMBER_OF_SUGGESTION)
    return res[first_post:first_post + NUMBER_OF_SUGGESTION]


def suggest_follow(*, account: Account) -> list:
    NUMBER_OF_SUGGESTION = 3
    user = get_user_account(account)

    comps = Company.objects.exclude(followers=user)
    if comps.count() < NUMBER_OF_SUGGESTION:
        return comps
    fst = randint(0, comps.count() - NUMBER_OF_SUGGESTION)
    return comps[fst:fst + NUMBER_OF_SUGGESTION]


def get_user_account(account: Account) -> User:
    e = User.objects.filter(account=account).first()
    if e is None:
        raise InvalidInputFormat("User not found!")
    return e
