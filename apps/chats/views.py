# Python
from typing import Any

# Django
from django.db.models import QuerySet

# Rest Framework
from rest_framework.request import Request as DRF_Request
from rest_framework.response import Response as DRF_Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.decorators import action
from rest_framework.status import HTTP_400_BAD_REQUEST

# Project
from abstracts.handlers import DRFResponseHandler
from abstracts.mixins import ModelInstanceMixin
from chats.models import Message
from chats.serializers import (
    MessageCreateSerializer,
    MessageDetailSerializer,
)
from auths.permission import (
    IsConnectedTelegram,
    IsNonDeletedUser,
)


class MessageViewSet(ModelInstanceMixin, DRFResponseHandler, ViewSet):
    """CustomUserViewSet."""

    queryset: Any = Message.objects
    permission_classes: tuple[Any] = (IsAuthenticated,)
    serializer_class: MessageDetailSerializer = MessageDetailSerializer

    def get_queryset(
        self,
        is_deleted: bool = False
    ) -> QuerySet[Message]:
        """Get deleted/non-deleted queryset with CustomUser instances."""
        return self.queryset.get_deleted() if is_deleted \
            else self.queryset.get_not_deleted()

    @action(
        methods=["POST"],
        url_path="upload_message",
        url_name="upload_message",
        detail=False,
        permission_classes=(
            IsAuthenticated,
            IsNonDeletedUser,
            IsConnectedTelegram,
        )
    )
    def upload_message(
        self,
        request: DRF_Request,
        *args: tuple[Any],
        **kwargs: dict[Any, Any]
    ) -> DRF_Response:
        """Handle POST-request to upload message."""
        serializer: MessageCreateSerializer = MessageCreateSerializer(
            data=request.data,
            context={"request": request}
        )
        valid: bool = serializer.is_valid()
        if valid:
            new_message: Message = serializer.save()
            return self.get_drf_response(
                request=request,
                data=new_message,
                serializer_class=self.serializer_class
            )
        return DRF_Response(
            data=serializer.errors,
            status=HTTP_400_BAD_REQUEST
        )
