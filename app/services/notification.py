import time

from app.models.account import Account
from app.models.company import Company
from app.models.user import User
from app.models.notification import Notification
from app.models.follow import Follow
from fcm_django.models import FCMDevice
from app.exceptions import InvalidInputFormat


def create_notification(*, type: str, account: Account, **kwargs):
    def new_notification(receiver: Account, content: str):
        n = Notification(
            type=type,
            account_id=account.id,
            receiver=receiver,
            content=content,
            post_job_id=kwargs.get('post_job_id') if 'post_job_id' in kwargs else 0,
            comment_id=kwargs.get('comment_id') if 'comment_id' in kwargs else 0,
            published_date=int(time.time())
        )
        n.save()

    def push_notification(receiver: Account, title: str, message: str):
        device = FCMDevice.objects.filter(user=receiver)
        for d in device:
            response = d.send_message(title=title, body=message, sound=True)
            print(response)

    def npost():
        u = get_user_account(account)
        content = u.firstname + ' ' + u.lastname + ' has just posted a new post.'

        followers = Follow.objects.filter(receiver=account)
        for f in followers:
            new_notification(receiver=f.sender, content=content)
            push_notification(
                receiver=f.sender,
                title=content,
                message='Tap to learn more.')

    def njob():
        c = get_company_account(account)
        content = c.name + ' has just listed a new job.'

        followers = Follow.objects.filter(receiver=account)
        for f in followers:
            new_notification(receiver=f.sender, content=content)
            push_notification(
                receiver=f.sender,
                title=content,
                message='Tap to learn more.')

    def ninterest():
        if 'receiver' not in kwargs:
            return
        u = get_user_account(account)
        content = u.firstname + ' ' + u.lastname + ' liked one of your posts.'
        new_notification(receiver=kwargs.get('receiver'), content=content)
        push_notification(
            receiver=kwargs.get('receiver'),
            title=content,
            message='Tap to view your post.')

    def ncomment():
        if 'receiver' not in kwargs:
            return
        u = get_user_account(account)
        content = u.firstname + ' ' + u.lastname + ' commented in one of your posts.'
        new_notification(receiver=kwargs.get('receiver'), content=content)
        push_notification(
            receiver=kwargs.get('receiver'),
            title=content,
            message='Tap to view your post.')

    def nfollow():
        if 'receiver' not in kwargs:
            return
        u = get_user_account(account)
        content = u.firstname + ' ' + u.lastname + ' followed you.'
        new_notification(receiver=kwargs.get('receiver'), content=content)
        push_notification(
            receiver=kwargs.get('receiver'),
            title=content,
            message='How about following them back?')

    switcher = {
        'post': npost,
        'job': njob,
        'interest': ninterest,
        'comment': ncomment,
        'follow': nfollow,
    }
    func = switcher.get(type)
    func()


def list_notification(*, account: Account, t: int) -> list:
    NUMBER_OF_NOTIFICATION = 20

    noti = Notification.objects.filter(
        receiver=account, published_date__lt=t).order_by('-published_date')
    return noti[:NUMBER_OF_NOTIFICATION]


def get_company_account(account: Account) -> Company:
    c = Company.objects.filter(account=account).first()
    if c is None:
        raise InvalidInputFormat("Company not found")
    return c


def get_user_account(account: Account) -> User:
    u = User.objects.filter(account=account).first()
    if u is None:
        raise InvalidInputFormat("User not found")
    return u
