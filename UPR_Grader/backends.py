from django.contrib.auth.backends import BaseBackend
from UPR_Grader.models import Students


class StudentsBackend(BaseBackend):
    def authenticate(self, email=None, password=None):
        try:
            student = Students.objects.get(student_email=email, student_password=password)
            if student:
                return student
        except Students.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Students.objects.get(pk=user_id)
        except Students.DoesNotExist:
            return None
