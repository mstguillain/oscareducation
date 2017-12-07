# explain : https://docs.djangoproject.com/en/1.11/topics/signals/#defining-signals

import django.dispatch

# Send a signal to prevent another app(s) that a student is added to Lesson (level)
student_added_to_lesson = django.dispatch.Signal(providing_args=["student", "level"])
