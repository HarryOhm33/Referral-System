# auth/middleware.py

from functools import wraps
from rest_framework.response import Response
from rest_framework import status


def isAdmin(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = request.user

        # -----------------------------------
        # Not logged in
        # -----------------------------------
        if not user:
            return Response(
                {"error": "Authentication required."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # -----------------------------------
        # Not admin
        # -----------------------------------
        if not getattr(user, "isAdmin", False):
            return Response(
                {"error": "Admin access required."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # -----------------------------------
        # OK
        # -----------------------------------
        return view_func(request, *args, **kwargs)

    return wrapper
