from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model


class StudentIDBackend(BaseBackend):
    def authenticate(self, request, first_name=None, last_name=None, student_id=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(first_name=first_name, last_name=last_name, student_id=student_id)
        except UserModel.DoesNotExist:
            return None

        return user

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
