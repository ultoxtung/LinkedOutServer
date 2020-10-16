from app.models.skill import Skill
from app.models.user import User
from app.models.account import Account
from app.exceptions import InvalidInputFormat


def list_skill(*, id: int) -> dict:
    user_exist(id)
    skills = User.objects.filter(account__id=id).first().skills.all()
    return {
        "skills": [s.name for s in skills]
    }


def create_skill(*, account: Account, skill: str) -> dict:
    user_exist(account.id)
    user_skill_not_exist(account.id, skill)
    s = Skill.objects.filter(name__iexact=skill).first()
    if s is None:
        raise InvalidInputFormat(
            "Skill with name {} does not exist in database.".format(skill))
    user = User.objects.filter(account__id=account.id).first()
    user.skills.add(s)
    return {
        "skills": [s.name for s in user.skills.all()]
    }


def delete_skill(*, account: Account, skill: str) -> dict:
    user_exist(account.id)
    user_skill_exist(account.id, skill)
    s = Skill.objects.filter(name__iexact=skill).first()
    if s is None:
        raise InvalidInputFormat(
            "Skill with name {} does not exist in database.".format(skill))
    user = User.objects.filter(account__id=account.id).first()
    user.skills.remove(s)
    return {
        "skills": [s.name for s in user.skills.all()]
    }


def user_exist(account_id: str, raise_exception=True) -> bool:
    s = User.objects.filter(account__id=account_id).first()
    if s is None:
        if raise_exception:
            raise InvalidInputFormat(
                "User with account id {} not found.".format(account_id))
        return False
    return True


def user_skill_exist(account_id: int, skill: str, raise_exception=True) -> bool:
    s = User.objects.filter(
        account__id=account_id).first().skills.filter(name__iexact=skill).first()
    if s is None:
        if raise_exception:
            raise InvalidInputFormat(
                "User has no skill '{}'.".format(s.name))
        return False
    return True


def user_skill_not_exist(account_id: int, skill: str, raise_exception=True) -> bool:
    s = User.objects.filter(
        account__id=account_id).first().skills.filter(name__iexact=skill).first()
    if s is not None:
        if raise_exception:
            raise InvalidInputFormat(
                "User already has skill '{}'.".format(s.name))
        return False
    return True
