import time
from django.db.models import Q

from app.models.message import Message
from app.models.account import Account
from app.models.company import Company
from app.models.user import User
from app.exceptions import InvalidInputFormat


NUMBER_OF_CONVERSATIONS = 20
NUMBER_OF_MESSAGES = 50


def send_message(*, account: Account, id: int, type: str, content: str):
    receiver = get_account_with_id(id=id)
    if receiver is None:
        return False
    m = Message(
        sender=account,
        receiver=receiver,
        type=type,
        content=content,
        published_date=int(time.time()),
    )
    m.save()
    return True


def get_last_message(*, first_user: Account, second_user: Account) -> Message:
    outgoing = Message.objects.filter(
        sender=first_user,
        receiver=second_user).order_by('-published_date').first()
    incoming = Message.objects.filter(
        sender=second_user,
        receiver=first_user).order_by('-published_date').first()

    if incoming is None:
        return outgoing
    if outgoing is None:
        return incoming
    return outgoing if outgoing.published_date > incoming.published_date else incoming


def list_conversation(*, account: Account, t: int) -> list:
    outgoing = Message.objects.filter(sender=account, published_date__lt=t)
    incoming = Message.objects.filter(receiver=account, published_date__lt=t)

    cons = []
    for c in outgoing:
        cons.append(c.receiver)
    for c in incoming:
        cons.append(c.sender)
    cons = list(dict.fromkeys(cons))

    res = []
    for c in cons:
        info = get_account_info(account=c)
        mess = get_last_message(first_user=account, second_user=c)
        res.append(
            {
                'id': info['id'],
                'name': info['name'],
                'profile_picture': info['profile_picture'],
                'last_message_content': mess.content,
                'last_message_timestamp': mess.published_date,
                'outgoing': (mess.sender == account),
            }
        )
    return sorted(res,
                  key=lambda instance: instance['last_message_timestamp'],
                  reverse=True)[:NUMBER_OF_CONVERSATIONS]


def get_conversation(*, account: Account, id: int, t: int) -> list:
    second_user = get_account_with_id(id=id)
    messages = Message.objects.filter(
        Q(Q(Q(sender=account) & Q(receiver=second_user)) |
          Q(Q(sender=second_user) & Q(receiver=account))) &
        Q(published_date__lt=t))
    return sorted(messages,
                  key=lambda instance: instance.published_date,
                  reverse=True)[:NUMBER_OF_MESSAGES]


def get_account_info(account: Account) -> dict:
    if (account.account_type == 'user'):
        u = User.objects.filter(account=account).first()
        if u is None:
            raise InvalidInputFormat('User not found')
        return {
            'id': account.id,
            'name': u.firstname + ' ' + u.lastname,
            'profile_picture': u.profile_picture,
        }
    else:
        c = Company.objects.filter(account=account).first()
        if c is None:
            raise InvalidInputFormat('Company not found')
        return {
            'id': account.id,
            'name': c.name,
            'profile_picture': c.profile_picture,
        }


def get_account_with_id(id: int) -> Account:
    a = Account.objects.filter(id=id).first()
    if a is None:
        raise InvalidInputFormat("Can't find user with id {}".format(id))
    return a
