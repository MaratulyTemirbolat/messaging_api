# Python
from typing import Optional, Any
from datetime import (
    datetime,
    timedelta
)

# Third party
from jwt import (
    encode,
    decode,
)
from jwt.exceptions import InvalidSignatureError

# Django
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser

# Rest Framework
from rest_framework.authentication import BaseAuthentication
from rest_framework.request import Request as DRF_Request
from rest_framework.exceptions import (
    AuthenticationFailed,
    ParseError,
)

CustomUser: AbstractBaseUser = get_user_model()


class JWTAuthentication(BaseAuthentication):
    """JWTAuthentication."""

    def __get_header_token(self, header_auth_value: str) -> str:
        list_value: list[str] = header_auth_value.split(" ")
        return list_value[1].strip() if len(list_value) == 2 else ""

    def authenticate(self, request: DRF_Request):
        header_auth_value: Optional[str] = request.META.get(
            "HTTP_AUTHORIZATION",
            None
        )
        telegram_key: Optional[str] = request.query_params.get("key", None)

        if not header_auth_value or not telegram_key:
            return None
        print(telegram_key, type(telegram_key))
        jwt_token = self.__get_header_token(
            header_auth_value=header_auth_value.strip()
        )
        payload: Any

        try:
            payload = decode(
                jwt=jwt_token,
                key=telegram_key,
                algorithms=['HS256']
            )
        except InvalidSignatureError:
            raise AuthenticationFailed(detail="Недопустимая подпись")
        except:  # noqa
            raise ParseError()

        breakpoint()

    def authenticate_header(self, request: DRF_Request) -> str:
        print("authenticate_header")
        return settings.JWT_HEADER_KEY

    @classmethod
    def create_jwt(cls, user: CustomUser):
        print("create_jwt")
        exp: int = int(
            (
                datetime.now() +
                timedelta(days=settings.JWT_CONF['TOKEN_LIFETIME_DAYS'])
            ).timestamp()
        )
        # payload: dict[str, Any] = {
        #     "user_identifier": user.login,
        #     'exp': exp,

        # }
