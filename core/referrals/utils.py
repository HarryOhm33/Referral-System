import random
import string


PREFIX = "SVH"


def generate_random_code(length=6):
    chars = string.ascii_uppercase + string.digits
    return "".join(random.choices(chars, k=length))


def build_referral_code():
    return f"{PREFIX}-{generate_random_code()}"
