# Python
from typing import (
    Any,
    Optional,
)

# Third party
from rest_framework_simplejwt.tokens import RefreshToken

# Django
from django.db.models import QuerySet
from django.contrib.auth import login

# Rest Framework
from rest_framework.request import Request as DRF_Request
from rest_framework.response import Response as DRF_Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework.decorators import action
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN,
)

# Project
from auths.models import CustomUser, CustomUserManager
from auths.serializers import (
    CustomUserCreateSerializer,
    CustomUserListSerializer,
    CustomUserLoginSerializer,
)
from auths.permission import (
    IsSuperUserRequestAdmin,
    IsNonDeletedUser,
)
from abstracts.utils import cast_to_int
from abstracts.handlers import DRFResponseHandler
from abstracts.mixins import ModelInstanceMixin
from chats.serializers import MessageForeignKeySerializer


class CustomUserViewSet(ModelInstanceMixin, DRFResponseHandler, ViewSet):
    """CustomUserViewSet."""

    queryset: CustomUserManager = CustomUser.objects
    permission_classes: tuple[Any] = (AllowAny,)
    serializer_class: CustomUserCreateSerializer = CustomUserCreateSerializer

    def get_queryset(
        self,
        is_deleted: bool = False
    ) -> QuerySet[CustomUser]:
        """Get deleted/non-deleted queryset with CustomUser instances."""
        return self.queryset.get_deleted() if is_deleted \
            else self.queryset.get_not_deleted()

    @action(
        methods=["POST"],
        url_path="register_user",
        url_name="user_registration",
        detail=False,
        permission_classes=(IsSuperUserRequestAdmin,)
    )
    def register_user(
        self,
        request: DRF_Request,
        *args: tuple[Any],
        **kwargs: dict[Any, Any]
    ) -> DRF_Response:
        """Handle POST-request to create/register new user."""
        is_superuser: bool = bool(
            request.data.get("is_superuser", False)
        )
        is_staff: bool = True if is_superuser else False
        serializer: CustomUserCreateSerializer = self.serializer_class(
            data=request.data
        )
        new_password: Optional[str] = request.data.get("password", None)
        valid: bool = serializer.is_valid()
        if valid:
            new_cust_user: CustomUser = CustomUser(
                **request.data,
                is_staff=is_staff
            )
            new_cust_user.set_password(raw_password=new_password)
            new_cust_user.save()
            login(
                request=request,
                user=new_cust_user
            )
            refresh_token: RefreshToken = RefreshToken.for_user(
                user=new_cust_user
            )
            det_ser: CustomUserListSerializer = CustomUserListSerializer(
                instance=new_cust_user,
                many=False
            )
            resulted_data: dict[str, Any] = det_ser.data.copy()
            resulted_data.setdefault("access", str(refresh_token.access_token))
            response: DRF_Response = DRF_Response(
                data=resulted_data,
                status=HTTP_200_OK
            )
            return response
        return DRF_Response(
            data=serializer.errors,
            status=HTTP_400_BAD_REQUEST
        )

    @action(
        methods=["GET"],
        url_path="messages",
        url_name="user_messages",
        detail=False,
        permission_classes=(IsAuthenticated, IsNonDeletedUser,)
    )
    def get_user_messages(
        self,
        request: DRF_Request,
        *args: tuple[Any],
        **kwargs: dict[Any, Any]
    ) -> DRF_Response:
        """Handle GET-request to obtain user messages."""
        return self.get_drf_response(
            request=request,
            data=request.user.messages.get_not_deleted(),
            serializer_class=MessageForeignKeySerializer,
            many=True
        )

    @action(
        methods=["POST"],
        url_path="login_user",
        url_name="login_user",
        detail=False,
        permission_classes=(AllowAny,)
    )
    def login_user(
        self,
        request: DRF_Request,
        *args: tuple[Any],
        **kwargs: dict[Any, Any]
    ) -> DRF_Response:
        """Handle POST-request to login into the system."""
        serializer: CustomUserLoginSerializer = CustomUserLoginSerializer(
            data=request.data
        )
        valid: bool = serializer.is_valid()
        if valid:
            prov_login: str = request.data.get("login", "")
            prov_password: str = request.data.get("password", "")

            user: Optional[CustomUser] = self.queryset.get_user_by_login(
                login=prov_login
            )

            if not user:
                return DRF_Response(
                    data={
                        "detail": "Пользователь с "
                        f"логином '{prov_login}' не найден"
                    },
                    status=HTTP_404_NOT_FOUND
                )

            same_passwords: bool = user.check_password(
                raw_password=prov_password
            )
            if not same_passwords:
                return DRF_Response(
                    data={"response": "Вы ввели неправильный пароль"},
                    status=HTTP_403_FORBIDDEN
                )
            if user.datetime_deleted:
                return DRF_Response(
                    data={"response": "Извините, но ваше пользователь удалён"},
                    status=HTTP_403_FORBIDDEN
                )
            login(
                request=request,
                user=user
            )
            refresh_token: RefreshToken = RefreshToken.for_user(user=user)
            det_ser: CustomUserListSerializer = CustomUserListSerializer(
                instance=user,
                many=False
            )
            resulted_data: dict[str, Any] = det_ser.data.copy()
            resulted_data.setdefault("access", str(refresh_token.access_token))
            response: DRF_Response = DRF_Response(
                data=resulted_data,
                status=HTTP_200_OK
            )
            return response

        return DRF_Response(
            data=serializer.errors,
            status=HTTP_400_BAD_REQUEST
        )

    @action(
        methods=["GET"],
        url_path="get_token",
        url_name="user_token",
        detail=False,
        permission_classes=(IsAuthenticated, IsNonDeletedUser,)
    )
    def get_token(
        self,
        request: DRF_Request,
        *args: tuple[Any],
        **kwargs: dict[Any, Any]
    ) -> DRF_Response:
        """Handle GET-request to obtain token."""
        refresh_token: RefreshToken = RefreshToken.for_user(user=request.user)
        response: DRF_Response = DRF_Response(
            data={
                "token": str(refresh_token.access_token),
            },
            status=HTTP_200_OK
        )
        return response

    @action(
        methods=["GET"],
        url_path="telegram_connect",
        url_name="telegram_connect",
        detail=False,
        permission_classes=(IsAuthenticated, IsNonDeletedUser,)
    )
    def connect_telegram(
        self,
        request: DRF_Request,
        *args: tuple[Any],
        **kwargs: dict[Any, Any]
    ) -> DRF_Response:
        """Handle GET-request for connection between telegram/django."""
        if request.user.telegram_id:
            return DRF_Response(
                data={
                    "detail": "Ваш телеграм уже подключён!"
                },
                status=HTTP_403_FORBIDDEN
            )

        telegram_id: Optional[int] = cast_to_int(
            value=request.query_params.get("chat_id", None)
        )
        if not telegram_id:
            return DRF_Response(
                data={
                    "detail": "Идентификатор чата должен "
                    "быть предоставлен в виде числа!"
                },
                status=HTTP_400_BAD_REQUEST
            )
        request.user.set_telegram_id(telegram_id)
        return DRF_Response(
            data={
                "detail": "Чат успешно подключён!"
            },
            status=HTTP_200_OK
        )
