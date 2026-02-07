import random
import bcrypt
import jwt
from decouple import config
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import User, Otp, Session
from datetime import datetime, timedelta
from utils.auth import authenticate

SECRET_KEY = config("JWT-SECRET")


def generate_otp():
    return str(random.randint(100000, 999999))


@api_view(["POST"])
def signup(request):
    name = request.data.get("name")
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password or not name:
        return Response(
            {"error": "Name, Email and password are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # 🔴 Delete any existing OTPs for this email
    Otp.objects(email=email).delete()

    User.objects(email=email, is_verified=False).delete()

    if User.objects(email=email, is_verified=True).first():
        return Response({"error": "User already exists."}, status=400)

    otp = generate_otp()

    # password hashing
    hash_pass = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    User(name=name, email=email, password=hash_pass, is_verified=False).save()
    Otp(email=email, otp=otp).save()

    # Send OTP via email
    send_mail(
        subject="Your OTP Code",
        message=f"Your OTP code is {otp}",
        from_email="gamesmugler95@gmail.com",
        recipient_list=[email],
        fail_silently=False,
    )

    return Response(
        {"valid": True, "message": "OTP sent to your email."},
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
def verify_otp(request):
    email = request.data.get("email")
    otp = request.data.get("otp")

    if not email or not otp:
        return Response(
            {"error": "Email and OTP are required."}, status=status.HTTP_400_BAD_REQUEST
        )

    otp_entry = Otp.objects(email=email, otp=otp).first()

    if not otp_entry:
        return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

    if otp_entry.expires_at < datetime.now():
        return Response(
            {"error": "OTP has expired."}, status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects(email=email).first()
    if not user:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    user.is_verified = True
    user.save()

    Otp.objects(email=email).delete()  # Delete used OTP

    return Response(
        {"valid": True, "message": "OTP verified successfully. You can now log in."},
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        return Response(
            {"error": "Email and password are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = User.objects(email=email, is_verified=True).first()
    if not user:
        return Response(
            {"error": "User not found or not verified."},
            status=status.HTTP_404_NOT_FOUND,
        )

    if not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        return Response(
            {"error": "Incorrect password."}, status=status.HTTP_401_UNAUTHORIZED
        )

    payload = {"user_id": str(user.id), "exp": datetime.now() + timedelta(days=7)}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    # Store token in Session model
    Session(user=user, token=token).save()

    response = Response(
        {
            "user": {
                "id": str(user.id),
                "name": user.name,
                "email": user.email,
                "is_verified": user.is_verified,
                "created_at": user.created_at.isoformat(),
            },
            "token": token,
        },
        status=status.HTTP_200_OK,
    )

    # Set token as HttpOnly cookie
    response.set_cookie(
        key="token",
        value=token,
        httponly=True,
        secure=True,  # Set to True in production with HTTPS
        samesite="Lax",  # Or 'Strict' depending on your use case
        max_age=7 * 24 * 60 * 60,  # 7 days
    )

    return response


@api_view(["POST"])
@authenticate
def verify_session(request):
    user = request.user  # set by your authenticate middleware

    return Response(
        {
            "valid": True,
            "user": {
                "id": str(user.id),
                "name": user.name,
                "email": user.email,
                "is_verified": user.is_verified,
                "created_at": user.created_at.isoformat(),
            },
        },
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@authenticate
def logout(request):
    token = request.token  # Set by your @authenticate decorator

    # Delete the session
    deleted = Session.objects(token=token).delete()

    response = Response(
        (
            {"valid": True, "message": "Logged out successfully."}
            if deleted
            else {"message": "Session not found."}
        ),
        status=status.HTTP_200_OK if deleted else status.HTTP_404_NOT_FOUND,
    )

    # Clear the token cookie
    response.delete_cookie("token")

    return response
