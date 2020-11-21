from django.db.models import Q
from django.db.models import Count

from app.models.user import User
from app.models.company import Company
from app.models.job import Job
from app.models.post import Post
from app.exceptions import InvalidInputFormat


def search(*, type: str, **kwargs) -> list:
    if type == 'company':
        return company_search(
            (kwargs.get('query') or '') if ('query' in kwargs) else '',
            (kwargs.get('specialties') or '') if ('specialties' in kwargs) else ''
        )
    elif type == 'user':
        return user_search(
            (kwargs.get('query') or '') if ('query' in kwargs) else '',
            (kwargs.get('skills') or '') if ('skills' in kwargs) else ''
        )
    elif type == 'job':
        return job_search(
            (kwargs.get('query') or '') if ('query' in kwargs) else '',
            (kwargs.get('skills') or '') if ('skills' in kwargs) else ''
        )
    elif type == 'post':
        return post_search(
            (kwargs.get('query') or '') if ('query' in kwargs) else ''
        )
    else:
        raise InvalidInputFormat("Invalid search type!")


def company_search(query: str, specialties: str) -> list:
    if specialties == '':
        companies_sw = Company.objects.filter(name__istartswith=query)
        companies_ct = Company.objects.filter(name__icontains=query)
    else:
        specialty_list = specialties.split(',')
        companies_sw = Company.objects.filter(name__istartswith=query, specialties__name__in=specialty_list).annotate(num_attr=Count('specialties')).filter(num_attr=len(specialty_list))
        companies_ct = Company.objects.filter(name__icontains=query, specialties__name__in=specialty_list).annotate(num_attr=Count('specialties')).filter(num_attr=len(specialty_list))

    return list(companies_sw.union(companies_ct, all=False))


def user_search(query: str, skills: str) -> list:
    print(skills)
    if skills == '':
        users_sw = User.objects.filter(Q(firstname__istartswith=query) | Q(lastname__istartswith=query))
        users_ct = User.objects.filter(Q(firstname__icontains=query) | Q(lastname__icontains=query))
    else:
        skill_list = skills.split(',')
        users_sw = User.objects.filter((Q(firstname__istartswith=query) | Q(lastname__istartswith=query)) & Q(skills__name__in=skill_list)).annotate(num_attr=Count('skills')).filter(num_attr=len(skill_list))
        users_ct = User.objects.filter((Q(firstname__icontains=query) | Q(lastname__icontains=query)) & Q(skills__name__in=skill_list)).annotate(num_attr=Count('skills')).filter(num_attr=len(skill_list))

    return list(users_sw.union(users_ct, all=False))


def job_search(query: str, skills: str) -> list:
    if skills == '':
        jobs_ct = Job.objects.filter(title__icontains=query).order_by('-published_date')
    else:
        skill_list = skills.split(',')
        jobs_ct = Job.objects.filter(title__icontains=query, skills__name__in=skill_list).annotate(num_attr=Count('skills')).filter(num_attr=len(skill_list)).order_by('-published_date')

    return list(jobs_ct)


def post_search(query: str) -> list:
    posts_ct = Post.objects.filter(content__icontains=query).order_by('-published_date')

    return list(posts_ct)
