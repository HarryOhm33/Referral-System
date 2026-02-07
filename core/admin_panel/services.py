from referrals.models import Referral, RewardLedger, RewardConfig


def get_top_referrers(limit=10):
    """
    Returns top users by successful referrals.
    """

    pipeline = [
        {"$match": {"referral_code_used": {"$ne": None}}},
        {
            "$group": {
                "_id": "$referred_by",
                "successful_referrals": {"$sum": 1},
            }
        },
        {"$sort": {"successful_referrals": -1}},
        {"$limit": limit},
    ]

    results = Referral.objects.aggregate(*pipeline)

    response = []

    for r in results:
        response.append(
            {
                "user_id": str(r["_id"]),
                "successful_referrals": r["successful_referrals"],
            }
        )

    return response


def credit_reward(reward_id):
    """
    Credit a pending reward.
    """

    reward = RewardLedger.objects(id=reward_id).first()

    if not reward:
        raise ValueError("Reward not found")

    if reward.status != "PENDING":
        raise ValueError("Only pending rewards can be credited")

    reward.status = "CREDITED"
    reward.save()

    return reward


def create_reward_config(data):
    """
    Create new reward configuration.
    """

    reward_type = data.get("reward_type")
    reward_value = data.get("reward_value")
    reward_unit = data.get("reward_unit")

    if not reward_type or not reward_value or not reward_unit:
        raise ValueError("Missing required fields")

    config = RewardConfig(
        reward_type=reward_type,
        reward_value=reward_value,
        reward_unit=reward_unit,
        is_active=True,
    )
    config.save()

    return config
