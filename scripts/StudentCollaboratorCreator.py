from users.models import Student
from student_collaboration.models import StudentCollaborator,CollaborativeSettings


def run():
    users = Student.objects.all()
    for user in users:
        collaborator = StudentCollaborator.objects.filter(user=user)
        if collaborator.count() < 1:
            StudentCollaborator.objects.create(user=user)