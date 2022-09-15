from flask import Blueprint, request
from util import generatedata, SUCCESS
from controllers.user import (
    create_user,
    email_verification,
    forget_password,
    resendEmailToken,
    reset_password,
    reset_token_status,
    log_in,
    log_out
)
from middleware import is_auth


userRoutes = Blueprint('userRoutes', __name__)

userRoutes.add_url_rule("/api/user/create",
                        view_func=create_user, methods=["POST"])

userRoutes.add_url_rule("/api/user/log-in", view_func=log_in, methods=["POST"])

userRoutes.add_url_rule("/api/user/verify-email",
                        view_func=email_verification, methods=["POST"])

userRoutes.add_url_rule("/api/user/resend-email-verification-token",
                        view_func=resendEmailToken, methods=["POST"])

userRoutes.add_url_rule("/api/user/forget-password",
                        view_func=forget_password, methods=["POST"])

userRoutes.add_url_rule("/api/user/verify-password-reset-token",
                        view_func=reset_token_status, methods=["POST"])

userRoutes.add_url_rule("/api/user/reset-password",
                        view_func=reset_password, methods=["POST"])

@userRoutes.route("/api/user/is-auth")
@is_auth
def auth_response():
    return generatedata(SUCCESS, request.user, 'is logged in'), 201

userRoutes.add_url_rule("/api/user/log-out",
                        view_func=log_out, methods=["DELETE"])
