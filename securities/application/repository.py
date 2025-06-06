from django.shortcuts import get_object_or_404

from .models import Application


def get_repository():
    return repo


def set_repository(new_repo):
    global repo
    repo = new_repo


def filter_getter(model_class, **kwargs):
    return model_class.objects.filter(**kwargs).first()


class Repository:

    def get_application_by_user(self, user, status=None, raise_404_if_not_exist=False):
        getter = filter_getter
        if raise_404_if_not_exist:
            getter = get_object_or_404
        if status:
            return getter(Application, user=user, status=status)
        return getter(Application, user=user)

    def save_application_and_update_status(self, form, user, status):
        app = form.save(commit=False)
        app.user = user
        app.status = status
        app.save()


repo = Repository()
