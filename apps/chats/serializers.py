# Rest Framework
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    DateTimeField,
    HiddenField,
    CurrentUserDefault,
)

# Project
from chats.models import Message
from abstracts.serializers import AbstractDateTimeSerializer
from auths.serializers import CustomUserForeignKeySerializer


class MessageForeignKeySerializer(AbstractDateTimeSerializer, ModelSerializer):
    """MessageForeignKeySerializer."""

    datetime_created: DateTimeField = \
        AbstractDateTimeSerializer.datetime_created
    is_deleted: SerializerMethodField = \
        AbstractDateTimeSerializer.is_deleted

    class Meta:
        """Customization of the serializer."""

        model: Message = Message
        fields: tuple[str] = (
            "id",
            "text",
            "owner",
            "datetime_created",
            "is_deleted",
        )


class MessageDetailSerializer(AbstractDateTimeSerializer, ModelSerializer):
    """MessageDetailSerializer."""

    datetime_created: DateTimeField = \
        AbstractDateTimeSerializer.datetime_created
    is_deleted: SerializerMethodField = \
        AbstractDateTimeSerializer.is_deleted
    owner: CustomUserForeignKeySerializer = CustomUserForeignKeySerializer()

    class Meta:
        """Customization of the serializer."""

        model: Message = Message
        fields: tuple[str] = (
            "id",
            "text",
            "owner",
            "datetime_created",
            "is_deleted",
        )


class MessageCreateSerializer(ModelSerializer):
    """MessageCreateSerializer."""

    owner: HiddenField = HiddenField(
        default=CurrentUserDefault()
    )

    class Meta:
        """Customization of the Serializer."""

        model: Message = Message
        fields: tuple[str] = (
            "text",
            "owner",
        )
