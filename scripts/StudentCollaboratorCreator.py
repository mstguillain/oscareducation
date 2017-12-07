from users.models import Student
from student_collaboration.models import StudentCollaborator
from promotions.models import Lesson, Stage

# the minimal degree where collaboration student should be allowed
MINIMAL_DEGREE = StudentCollaborator.MINIMAL_DEGREE


def run():
    # the classroom(s) where this query should be run
    lessons = Lesson.objects.filter(stage__level__gte=MINIMAL_DEGREE)
    if lessons:
        users_id = lessons.values_list('students__pk', flat=True)
        users = Student.objects.filter(pk__in=users_id).all()
        print("FOUND", str(lessons.count()), "classroom(s)")
        for user in users.all():
            collaborator = StudentCollaborator.objects.filter(user=user)
            if collaborator.count() < 1:
                StudentCollaborator.objects.create(user=user)
