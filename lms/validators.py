from rest_framework import serializers


def validate_youtube_url(value):
    """
    Разрешаем только ссылки на YouTube.
    Всё остальное запрещено.
    """
    if value is None or value == "":
        return value

    allowed_domains = ["youtube.com", "youtu.be"]

    if not any(domain in value for domain in allowed_domains):
        raise serializers.ValidationError(
            "Разрешены только ссылки на YouTube."
        )

    return value