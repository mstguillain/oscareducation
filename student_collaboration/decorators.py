from django.core.exceptions import PermissionDenied


def user_has_collaborative_tool_active(function):
    def wrap(request, *args, **kwargs):
        collaborative_tool = request.user.student.studentcollaborator.collaborative_tool;
        if collaborative_tool:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
