def referral_to_dict(referral):
    return {
        "id": str(referral.id),
        "referral_code": referral.referral_code,
        "referred_by": str(referral.referred_by.id),
    }


def apply_referral_request(data):
    code = data.get("referral_code")

    if not code:
        raise ValueError("referral_code required")

    return code
