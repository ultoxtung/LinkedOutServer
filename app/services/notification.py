import time

from app.models.account import Account
from app.models.company import Company
from app.models.user import User
from app.models.notification import Notification
from app.models.follow import Follow
from app.models.post import Post
from app.models.job import Job
from fcm_django.models import FCMDevice
from app.exceptions import InvalidInputFormat


MAX_NOTIFICATION_LENGTH = 100    # in characters


def create_notification(*, type: str, account: Account, **kwargs):
    def new_notification(receiver: Account, author_name: str, content: str):
        n = Notification(
            type=type,
            account_id=account.id,
            receiver=receiver,
            content='',
            post_job_id=kwargs.get('post_job_id') if 'post_job_id' in kwargs else 0,
            comment_id=kwargs.get('comment_id') if 'comment_id' in kwargs else 0,
            published_date=int(time.time())
        )
        n.save()

        if len(content) > MAX_NOTIFICATION_LENGTH:
            content = content[ : (MAX_NOTIFICATION_LENGTH - 3)] + '...'
        devices = FCMDevice.objects.filter(user=receiver)
        for d in devices:
            response = d.send_message(title=author_name, body=content, sound=True)
            # print(response)

    def npost():
        if 'post_job_id' not in kwargs:
            return
        u = get_user_account(account)
        author_name = u.firstname + ' ' + u.lastname
        p = Post.objects.filter(id=kwargs.get('post_job_id')).first()
        content = author_name + ' has just posted a new post: ' + p.content

        followers = Follow.objects.filter(receiver=account)
        for f in followers:
            new_notification(receiver=f.sender, author_name=author_name, content=content)

    def njob():
        if 'post_job_id' not in kwargs:
            return
        c = get_company_account(account)
        author_name = c.name
        j = Job.objects.filter(id=kwargs.get('post_job_id')).first()
        content = author_name + ' has just listed a new job: ' + j.title

        followers = Follow.objects.filter(receiver=account)
        for f in followers:
            new_notification(receiver=f.sender, author_name=author_name, content=content)

    def ninterest():
        if ('receiver' not in kwargs) or ('post_job_id' not in kwargs):
            return
        if (kwargs.get('receiver') == account):
            return
        u = get_user_account(account)
        author_name = u.firstname + ' ' + u.lastname
        p = Post.objects.filter(id=kwargs.get('post_job_id')).first()
        content = author_name + ' liked your post: ' + p.content
        new_notification(receiver=kwargs.get('receiver'),
                         author_name=author_name,
                         content=content)

    def ncomment():
        if ('receiver' not in kwargs) or ('post_job_id' not in kwargs):
            return
        if (kwargs.get('receiver') == account):
            return
        u = get_user_account(account)
        author_name = u.firstname + ' ' + u.lastname
        p = Post.objects.filter(id=kwargs.get('post_job_id')).first()
        content = author_name + ' commented on your post: ' + p.content
        new_notification(receiver=kwargs.get('receiver'),
                         author_name=author_name,
                         content=content)

    def nfollow():
        if 'receiver' not in kwargs:
            return
        if (kwargs.get('receiver') == account):
            return
        u = get_user_account(account)
        author_name = u.firstname + ' ' + u.lastname
        content = author_name + ' followed you. How about following them back?'
        new_notification(receiver=kwargs.get('receiver'),
                         author_name=author_name,
                         content=content)

    switcher = {
        'post': npost,
        'job': njob,
        'interest': ninterest,
        'comment': ncomment,
        'follow': nfollow,
    }
    func = switcher.get(type)
    func()


def list_notification(*, account: Account, t: int = 0) -> list:
    NUMBER_OF_NOTIFICATION = 20

    def get_author_name(type: str, id: int) -> str:
        if type == 'job':
            c = Company.objects.filter(account__id=id).first()
            return ('' if c is None else c.name)
        else:
            u = User.objects.filter(account__id=id).first()
            return ('' if u is None else u.firstname + ' ' + u.lastname)

    def get_profile_picture(type: str, id: int):
        if type == 'job':
            c = Company.objects.filter(account__id=id).first()
        else:
            c = User.objects.filter(account__id=id).first()
        return c.profile_picture

    def get_action(type: str) -> str:
        switcher = {
            'post': 'has just posted a new post',
            'job': 'has just listed a new job',
            'interest': 'liked your post',
            'comment': 'commented on your post',
            'follow': 'followed you',
        }
        return switcher.get(type)

    def get_content(type: str, id: int) -> str:
        if type in ['follow']:
            return ''
        elif type in ['post', 'interest', 'comment']:
            p = Post.objects.filter(id=id).first()
            return ('' if p is None else p.content)
        elif type in ['job']:
            j = Job.objects.filter(id=id).first()
            return ('' if j is None else j.title)
        else:
            return ''

    ts = t if t != 0 else int(time.time())
    noti = Notification.objects.filter(
        receiver=account, published_date__lt=ts).order_by('-published_date')
    return [
        {
            'id': n.id,
            'type': n.type,
            'author_name': get_author_name(n.type, n.account_id),
            'profile_picture': get_profile_picture(n.type, n.account_id),
            'action': get_action(n.type),
            'content': get_content(n.type, n.post_job_id),
            'post_job_id': n.post_job_id,
            'comment_id': n.comment_id,
            'published_date': n.published_date,
        } for n in noti[:NUMBER_OF_NOTIFICATION]
    ]


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
