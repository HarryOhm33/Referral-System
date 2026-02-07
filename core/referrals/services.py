from mongoengine.errors import NotUniqueError
from .models import Referral, RewardConfig, RewardLedger
from datetime import datetime
from .utils import build_referral_code


def generate_referral_for_user(user):
    # Idempotent: If user already has code → return it. Else create new.

    # check existing
    existing = Referral.objects(referred_by=user).first()
    if existing:
        return existing

    # create new with retry (collision safe)
    for _ in range(5):
        try:
            referral = Referral(
                referral_code=build_referral_code(),
                referred_by=user,
            )
            referral.save()
            return referral

        except NotUniqueError:
            # retry with new code
            continue

    raise Exception("Could not generate unique referral code")


def apply_referral_code(user, code):
    """
    Apply referral for a user.
    """

    # -------------------------------------------------
    # 1. find referral
    # -------------------------------------------------
    referral = Referral.objects(referral_code=code).first()
    if not referral:
        raise ValueError("Invalid referral code")

    # -------------------------------------------------
    # 2. prevent self referral
    # -------------------------------------------------
    if referral.referred_by.id == user.id:
        raise ValueError("You cannot use your own referral code")

    # -------------------------------------------------
    # 3. already used by someone
    # -------------------------------------------------
    if referral.referral_code_used:
        raise ValueError("Referral code already used")

    # -------------------------------------------------
    # 4. user already used any code?
    # -------------------------------------------------
    already_used = Referral.objects(referral_code_used=user).first()
    if already_used:
        raise ValueError("You have already used a referral")

    # -------------------------------------------------
    # 5. mark as used
    # -------------------------------------------------
    referral.referral_code_used = user
    referral.referral_used_at = datetime.utcnow()
    referral.save()

    # -------------------------------------------------
    # 6. fetch reward config
    # -------------------------------------------------
    config = RewardConfig.objects(reward_type="SIGNUP", is_active=True).first()

    if not config:
        raise ValueError("Reward config missing")

    # -------------------------------------------------
    # 7. prevent duplicate reward
    # -------------------------------------------------
    existing_reward = RewardLedger.objects(
        user=referral.referred_by,
        referral=referral,
        reward_type="SIGNUP",
    ).first()

    if existing_reward:
        return referral

    # -------------------------------------------------
    # 8. create PENDING reward for referrer
    # -------------------------------------------------
    RewardLedger(
        user=referral.referred_by,
        referral=referral,
        reward_type=config.reward_type,
        reward_value=config.reward_value,
        reward_unit=config.reward_unit,
        status="PENDING",
    ).save()

    return referral


def get_referral_summary(user):
    """
    Returns analytics summary for user's referral performance.
    """

    # -----------------------------------
    # find user's referral code
    # -----------------------------------
    my_referral = Referral.objects(referred_by=user).first()

    if not my_referral:
        return {
            "my_referral_code": None,
            "total_referrals": 0,
            "successful_referrals": 0,
            "conversion_rate": "0%",
        }

    # -----------------------------------
    # total referrals
    # -----------------------------------
    total = Referral.objects(referred_by=user).count()

    # -----------------------------------
    # successful referrals
    # -----------------------------------
    success = Referral.objects(referred_by=user, referral_code_used__ne=None).count()

    # -----------------------------------
    # conversion rate
    # -----------------------------------
    rate = 0
    if total > 0:
        rate = int((success / total) * 100)

    return {
        "my_referral_code": my_referral.referral_code,
        "total_referrals": total,
        "successful_referrals": success,
        "conversion_rate": f"{rate}%",
    }


def get_referral_list(user):
    """
    List of users who used my referral code.
    """

    referrals = Referral.objects(referred_by=user)

    result = []

    for r in referrals:
        if r.referral_code_used:
            status = "SUCCESS"
            used_by = str(r.referral_code_used.id)
            used_at = r.referral_used_at
        else:
            status = "PENDING"
            used_by = None
            used_at = None

        result.append(
            {
                "used_by_user_id": used_by,
                "used_at": used_at,
                "status": status,
            }
        )

    return result


def get_referral_timeline(user):
    """
    Returns successful referrals grouped by date.
    """

    pipeline = [
        {
            "$match": {
                "referred_by": user.id,
                "referral_code_used": {"$ne": None},
            }
        },
        {
            "$group": {
                "_id": {
                    "year": {"$year": "$referral_used_at"},
                    "month": {"$month": "$referral_used_at"},
                    "day": {"$dayOfMonth": "$referral_used_at"},
                },
                "count": {"$sum": 1},
            }
        },
        {"$sort": {"_id": 1}},
    ]

    results = Referral.objects.aggregate(*pipeline)

    response = []

    for r in results:
        d = r["_id"]
        date = datetime(d["year"], d["month"], d["day"]).strftime("%Y-%m-%d")

        response.append(
            {
                "date": date,
                "count": r["count"],
            }
        )

    return response


def get_reward_history(user):
    """
    Returns all rewards for logged-in user.
    """

    rewards = RewardLedger.objects(user=user).order_by("-created_at")

    result = []

    for r in rewards:
        result.append(
            {
                "reward_id": str(r.id),
                "reward_type": r.reward_type,
                "reward_value": r.reward_value,
                "reward_unit": r.reward_unit,
                "status": r.status,
                "created_at": r.created_at,
            }
        )

    return result
