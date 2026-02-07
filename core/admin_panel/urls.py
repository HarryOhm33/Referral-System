from django.urls import path
from .views import admin_top_referrers, admin_credit_reward, admin_create_reward_config

urlpatterns = [
    path("referrals/top/", admin_top_referrers, name="admin-top-referrers"),
    path(
        "rewards/<str:reward_id>/credit",
        admin_credit_reward,
        name="admin-credit-reward",
    ),
    path(
        "reward-config/create/",
        admin_create_reward_config,
        name="admin-create-reward-config",
    ),
]
