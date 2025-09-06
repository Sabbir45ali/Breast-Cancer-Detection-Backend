from django.urls import path
from .views import (
    signup_user, login_user,
    signup_org, login_org,
    login_admin,
    send_otp, verify_otp, forgot_password, reset_password
)

urlpatterns = [
    # User routes
    path("signup-user/", signup_user, name="signup_user"),
    path("login-user/", login_user, name="login_user"),

    # Organization routes
    path("signup-org/", signup_org, name="signup_org"),
    path("login-org/", login_org, name="login_org"),

    # Admin route
    path("login-admin/", login_admin, name="login_admin"),

    # OTP + Password Reset routes
    path("send-otp/", send_otp, name="send_otp"),
    path("forgot-password/", forgot_password, name="forgot_password"),
    path("verify-otp/", verify_otp, name="verify_otp"),
    path("reset-password/", reset_password, name="reset_password"),
]
