from app.models.post import Post
from app.models.account import Account
from app.models.user import User
from app.services.notification import create_notification
from app.exceptions import InvalidInputFormat


def check_interest(*, account: Account, id: int) -> bool:
    p = Post.objects.filter(id=id).first()
    if not p:
        raise InvalidInputFormat("Post with id {} doesn't exist.".format(id))
        return { 'interested': False }
    else:
        if p.interested_users.filter(account=account).exists():
            return { 'interested': True }
        return { 'interested': False }


def create_interest(*, account: Account, id: int) -> bool:
    p = Post.objects.filter(id=id).first()
    if not p:
        raise InvalidInputFormat("Post with id {} doesn't exist.".format(id))
        return { 'interested': False }

    user_account = get_user_account(account)
    if p.interested_users.filter(account=account).exists():
        raise InvalidInputFormat("User with id {} already interested post with id {}.".format(account.id, id))
    p.interested_users.add(user_account)
    create_notification(
        type='interest', account=account, post_job_id=id, receiver=p.user.account)

    return { 'interested': True }


def delete_interest(*, account: Account, id: int) -> bool:
    p = Post.objects.filter(id=id).first()
    if not p:
        raise InvalidInputFormat("Post with id {} doesn't exist.".format(id))
        return { 'interested': False }

    user_account = get_user_account(account)
    if not p.interested_users.filter(account=account).exists():
        raise InvalidInputFormat("User with id {} hasn't interested post with id {} yet.".format(account.id, id))
    p.interested_users.remove(user_account)
    return { 'interested': False }


def count_interest(*, account: Account, id: int) -> dict:
    p = Post.objects.filter(id=id).first()
    if not p:
        raise InvalidInputFormat("Post with id {} doesn't exist.".format(id))
        return { 'count': 0 }
    return {
        'count': p.interested_users.count()
    }


def account_interested(*, account: Account, id: int) -> list:
    p = Post.objects.filter(id=id).first()
    if not p:
        raise InvalidInputFormat("Post with id {} doesn't exist.".format(id))
    return [
        {
            'id': s.account.id,
            'firstname': s.firstname,
            'lastname': s.lastname,
            'profile_picture': s.profile_picture,
        } for s in p.interested_users.all()
    ]


def post_interested(*, account: Account, id: int) -> list:
    posts = Post.objects.filter(interested_users=get_user_with_id(id))
    return [
        {
            'id': p.id,
            'title': p.title,
            'content': p.content,
            'interest_count': p.interested_users.count(),
        } for p in posts
    ]


def get_user_account(account: Account) -> User:
    e = User.objects.filter(account=account).first()
    if e is None:
        raise InvalidInputFormat("User not found!")
    return e


def get_user_with_id(id: int) -> User:
    return User.objects.filter(account__id=id).first()
