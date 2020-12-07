from app.exceptions import InvalidInputFormat
from app.models.account import Account
from app.models.company import Company
from app.models.user import User
from app.models.follow import Follow
from app.services.notification import create_notification


def list_follow(*, account: Account, id: int) -> list:
    a = Account.objects.filter(id=id).first()
    if not a:
        raise InvalidInputFormat(
            "Account with id {} doesn't exist.".format(id))
    follows = Follow.objects.filter(receiver__id=id)
    accounts = [f.sender for f in follows]
    users = [User.objects.filter(account=a).first() for a in accounts]
    return [
        {
            'id': u.account.id,
            'firstname': u.firstname,
            'lastname': u.lastname,
            'profile_picture': u.profile_picture,
            'description': u.description,
            'followed_count': Follow.objects.filter(receiver=u.account).count(),
        } for u in users
    ]


def check_follow(*, account: Account, id: int) -> dict:
    a = Account.objects.filter(id=id).first()
    if not a:
        raise InvalidInputFormat(
            "Account with id {} doesn't exist.".format(id))
    if Follow.objects.filter(sender=account, receiver=a).exists():
        return {'followed': True}
    return {'followed': False}


def create_follow(*, account: Account, id: int) -> dict:
    a = Account.objects.filter(id=id).first()
    if not a:
        raise InvalidInputFormat(
            "Account with id {} doesn't exist.".format(id))

    if Follow.objects.filter(sender=account, receiver=a).exists():
        raise InvalidInputFormat(
            "Account with id {} already followed account with id {}.".format(account.id, id))
    new_follow = Follow(sender=account, receiver=a).save()
    create_notification(type='follow', account=account, receiver=a)

    return {'followed': True}


def delete_follow(*, account: Account, id: int) -> dict:
    a = Account.objects.filter(id=id).first()
    if not a:
        raise InvalidInputFormat(
            "Account with id {} doesn't exist.".format(id))

    f = Follow.objects.filter(sender=account, receiver=a)
    if not f:
        raise InvalidInputFormat(
            "Account with id {} has not followed account with id {} yet.".format(account.id, id))
    f.delete()
    return {'followed': False}


def count_follow(*, account: Account, id: int) -> dict:
    a = Account.objects.filter(id=id).first()
    if not a:
        raise InvalidInputFormat(
            "Account with id {} doesn't exist.".format(id))
    return {
        'count': Follow.objects.filter(receiver=a).count()
    }


def count_followed(*, account: Account, id: int) -> dict:
    a = Account.objects.filter(id=id).first()
    if not a:
        raise InvalidInputFormat(
            "Account with id {} doesn't exist.".format(id))
    return {
        'count': Follow.objects.filter(sender=a).count()
    }


def company_followed(*, account: Account, id: int) -> list:
    follows = Follow.objects.filter(
        sender__id=id, receiver__account_type='company')
    accounts = [f.receiver for f in follows]
    companies = [Company.objects.filter(account=a).first() for a in accounts]
    return [
        {
            'id': c.account.id,
            'name': c.name,
            'profile_picture': c.profile_picture,
            'description': c.description,
            'followed_count': Follow.objects.filter(receiver=c.account).count(),
        } for c in companies
    ]


def user_followed(*, account: Account, id: int) -> list:
    follows = Follow.objects.filter(
        sender__id=id, receiver__account_type='user')
    accounts = [f.receiver for f in follows]
    users = [User.objects.filter(account=a).first() for a in accounts]
    return [
        {
            'id': u.account.id,
            'firstname': u.firstname,
            'lastname': u.lastname,
            'profile_picture': u.profile_picture,
            'description': u.description,
            'followed_count': Follow.objects.filter(receiver=u.account).count(),
        } for u in users
    ]
