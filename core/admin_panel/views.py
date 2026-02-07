from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from utils.isAdmin import isAdmin as is_admin
from utils.auth import authenticate
from .services import get_top_referrers, credit_reward, create_reward_config


@api_view(["GET"])
@authenticate
@is_admin
def admin_top_referrers(request):

    data = get_top_referrers()
    return Response(data, status=status.HTTP_200_OK)


@api_view(["POST"])
@authenticate
@is_admin
def admin_credit_reward(request, reward_id):

    try:
        reward = credit_reward(reward_id)

        return Response(
            {
                "message": "Reward credited successfully",
                "reward_id": str(reward.id),
                "status": reward.status,
            },
            status=status.HTTP_200_OK,
        )

    except ValueError as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["POST"])
@authenticate
@is_admin
def admin_create_reward_config(request):
    try:
        config = create_reward_config(request.data)

        return Response(
            {
                "message": "Reward config created",
                "id": str(config.id),
                "reward_type": config.reward_type,
                "reward_value": config.reward_value,
                "reward_unit": config.reward_unit,
                "is_active": config.is_active,
            },
            status=status.HTTP_201_CREATED,
        )

    except ValueError as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST,
        )
