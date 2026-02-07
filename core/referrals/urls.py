from django.urls import path
from .views import (
    generate_referral,
    apply_referral,
    referral_summary,
    referral_list,
    referral_timeline,
    reward_history,
)

urlpatterns = [
    path("generate/", generate_referral, name="generate-referral"),
    path("apply/", apply_referral, name="apply-referral"),
    path("analytics/summary/", referral_summary, name="referral-summary"),
    path("analytics/list/", referral_list, name="referral-list"),
    path("analytics/timeline/", referral_timeline, name="referral-timeline"),
    path("rewards/history/", reward_history, name="reward-history"),
]
