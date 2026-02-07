from mongoengine import (
    Document,
    EmailField,
    StringField,
    BooleanField,
    DateTimeField,
    ReferenceField,
)
from datetime import datetime, timedelta


class User(Document):
    name = StringField(required=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    is_verified = BooleanField(default=False)
    isAdmin = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.now)

    meta = {"collection": "users"}


class Otp(Document):
    email = StringField(required=True)
    otp = StringField(required=True)
    created_at = DateTimeField(default=datetime.now)
    expires_at = DateTimeField(default=lambda: datetime.now() + timedelta(minutes=5))

    meta = {
        "collection": "otps",
        "indexes": [{"fields": ["created_at"], "expireAfterSeconds": 300}],
    }


class Session(Document):
    user = ReferenceField(User, required=True)
    token = StringField(required=True)
    created_at = DateTimeField(default=datetime.now)

    meta = {
        "indexes": [
            {
                "fields": ["created_at"],
                "expireAfterSeconds": 604800,  # 7 days in seconds
            }
        ]
    }
