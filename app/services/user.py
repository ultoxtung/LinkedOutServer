import os

from app.exceptions import InvalidInputFormat
from app.models.account import Account
from app.models.user import User
from backend.settings import MEDIA_ROOT


def get_user(*, id: int) -> User:
    s = User.objects.filter(account__id=id).first()
    if s is None:
        raise InvalidInputFormat(
            "User with account id {} not found.".format(id))
    return s


def create_user(*, account: Account, firstname: str, lastname: str, dateofbirth: str, gender: str, **kwargs) -> User:
    user_account_check(account)
    if user_exist(account.id, raise_exception=False):
        raise InvalidInputFormat(
            "Account {} already has a user.".format(account.id))
    profile_picture = None
    if gender.lower() == "male":
        profile_picture = 'profile/user_default_male.jpg'
    elif gender.lower() == "female":
        profile_picture = 'profile/user_default_female.jpg'
    elif gender.lower() == "other":
        profile_picture = 'profile/user_default_other.jpg'
    else:
        profile_picture = 'profile/user_default_other.jpg'
        print("Gender {} ???".format(gender))
    s = User(account=account, firstname=firstname, lastname=lastname,
             dateofbirth=dateofbirth, gender=gender, profile_picture=profile_picture, **kwargs)
    s.save()
    return s


def update_user(*, account: Account, firstname: str, lastname: str, dateofbirth: str, gender: str, **kwargs) -> User:
    user_account_check(account)
    user_exist(account.id)
    s = User.objects.filter(account=account)
    s.update(account=account, firstname=firstname, lastname=lastname,
             dateofbirth=dateofbirth, gender=gender, **kwargs)
    return s.first()


def set_profile_picture(account: Account, file_instance):
    user_exist(account.id)
    if file_instance.name.split('.')[-1] not in ['png', 'jpg', 'jpeg']:
        raise InvalidInputFormat(
            "File extension must be 'png', 'jpg' or 'jpeg'")
    s = User.objects.get(account__id=account.id)
    if s.profile_picture != User._meta.get_field('profile_picture').get_default():
        old_file_path = os.path.join(MEDIA_ROOT, s.profile_picture.name)
        if os.path.exists(old_file_path):
            os.remove(old_file_path)
    s.profile_picture.save(file_instance.name, file_instance, save=True)


def user_exist(account_id: str, raise_exception=True) -> bool:
    s = User.objects.filter(account__id=account_id).first()
    if s is None:
        if raise_exception:
            raise InvalidInputFormat(
                "User with account id {} not found.".format(account_id))
        return False
    return True


def user_account_check(account: Account, raise_exception=True):
    if account.account_type != 'user':
        if raise_exception:
            raise InvalidInputFormat(
                'Account {} is not a user account.'.format(account.id))
        return False
    return True
