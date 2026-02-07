import uuid
from datetime import datetime
from mongoengine import (
    Document,
    StringField,
    ReferenceField,
    DateTimeField,
    BooleanField,
    IntField,
    CASCADE,
    NULLIFY,
)

# import your user model
from user_auth.models import User


class Referral(Document):
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))

    referral_code = StringField(required=True, unique=True)

    # owner of code
    referred_by = ReferenceField(User, reverse_delete_rule=CASCADE)

    referred_at = DateTimeField(default=datetime.utcnow)

    # who used it
    referral_code_used = ReferenceField(User, null=True, reverse_delete_rule=NULLIFY)
    referral_used_at = DateTimeField()

    meta = {
        "indexes": [
            "referred_by",
            "referral_code_used",
            "referral_code",
        ]
    }


class RewardConfig(Document):

    REWARD_TYPES = ("SIGNUP", "FIRST_ORDER")
    UNITS = ("POINTS", "CASH")

    reward_type = StringField(choices=REWARD_TYPES, required=True)
    reward_value = IntField(required=True)
    reward_unit = StringField(choices=UNITS, required=True)

    is_active = BooleanField(default=True)

    created_at = DateTimeField(default=datetime.utcnow)


class RewardLedger(Document):

    STATUS = ("PENDING", "CREDITED", "REVOKED")

    user = ReferenceField(User, reverse_delete_rule=CASCADE)
    referral = ReferenceField(Referral, reverse_delete_rule=CASCADE)

    reward_type = StringField(required=True)
    reward_value = IntField(required=True)
    reward_unit = StringField(required=True)

    status = StringField(choices=STATUS, default="PENDING")

    created_at = DateTimeField(default=datetime.utcnow)

    meta = {
        "indexes": [
            "user",
        ]
    }
