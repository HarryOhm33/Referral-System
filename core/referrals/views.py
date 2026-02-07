from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from utils.auth import authenticate
from rest_framework import status

from .services import (
    generate_referral_for_user,
    apply_referral_code,
    get_referral_summary,
    get_referral_list,
    get_referral_timeline,
    get_reward_history,
)
from .serializers import referral_to_dict


@api_view(["POST"])
@authenticate
def generate_referral(request):
    user = request.user

    referral = generate_referral_for_user(user)

    return Response(referral_to_dict(referral))


@api_view(["POST"])
@authenticate
def apply_referral(request):
    try:
        code = request.data.get("referral_code")

        referral = apply_referral_code(request.user, code)

        return Response(
            {
                "message": "Referral applied successfully",
                "referral_code": referral.referral_code,
            }
        )

    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@authenticate
def referral_summary(request):
    data = get_referral_summary(request.user)
    return Response(data)


@api_view(["GET"])
@authenticate
def referral_list(request):
    data = get_referral_list(request.user)
    return Response(data)


@api_view(["GET"])
@authenticate
def referral_timeline(request):
    data = get_referral_timeline(request.user)
    return Response(data)


@api_view(["GET"])
@authenticate
def reward_history(request):
    data = get_reward_history(request.user)
    return Response(data)
