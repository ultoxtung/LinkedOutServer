from app.models.post import Post
from app.models.comment import Comment
from app.models.user import User
from app.models.account import Account
from app.exceptions import InvalidInputFormat


def list_comment(*, id: int) -> list:
    return Comment.objects.filter(post__id=id)


def create_comment(*, account: Account, id: int, content: str) -> list:
    user_account_check(account)
    c = Comment(
        user=get_user_account(account),
        post=get_post(id),
        content=content,
    )
    c.save()
    return list_comment(id=id)


def update_comment(*, account: Account, id: int, content: str) -> list:
    user_account_check(account)
    c = Comment.objects.filter(id=id)
    if not c:
        raise InvalidInputFormat("Comment with id {} not found".format(id))
    author_check(account, id)
    c.update(
        content=content,
    )
    post_id = c.first().post.id
    return list_comment(id=post_id)


def delete_comment(*, account: Account, id: int) -> list:
    user_account_check(account)
    c = Comment.objects.filter(id=id).first()
    if c is None:
        raise InvalidInputFormat("Comment with id {} not found".format(id))
    author_check(account, id)
    post_id = c.post.id
    c.delete()
    return list_comment(id=post_id)


def user_account_check(account: Account, raise_exception=True):
    if account.account_type != 'user':
        if raise_exception:
            raise InvalidInputFormat('Account {} is not a user account.'.format(account.id))
        return False
    return True


def get_user_account(account: Account) -> User:
    p = User.objects.filter(account=account).first()
    if p is None:
        raise InvalidInputFormat("User not found!")
    return p


def get_post(id: int) -> Post:
    p = Post.objects.filter(id=id).first()
    if p is None:
        raise InvalidInputFormat("Post not found!")
    return p


def author_check(account: Account, id: int) -> bool:
    c = Comment.objects.filter(id=id).first()
    if c.user != get_user_account(account):
        raise InvalidInputFormat('Account with id {} isn\'t author of comment with id {}'.format(account.id, id))
        return False
    return True
