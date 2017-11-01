from django.contrib.auth.models import User
from student_collaboration.models import StudentCollaborator,CollaborativeSettings


def run():
    users = User.objects.all()
    for user in users:
        collaborator = StudentCollaborator.objects.filter(user=user)
        if collaborator.count() < 1:
            settings = CollaborativeSettings.objects.create()
            StudentCollaborator.objects.create(user=user, settings=settings)