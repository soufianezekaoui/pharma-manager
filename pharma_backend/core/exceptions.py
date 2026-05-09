"""
Custom exception handler for uniform API error responses.
"""
import logging

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Return a consistent JSON error envelope:
    {
        "success": false,
        "message": "...",
        "errors": {...}   # optional
    }
    """
    # Let DRF handle standard exceptions first
    response = exception_handler(exc, context)

    if response is not None:
        data = {
            "success": False,
            "message": _extract_message(response.data),
            "errors": response.data,
        }
        response.data = data
        return response

    # Handle Django's own ValidationError
    if isinstance(exc, DjangoValidationError):
        return Response(
            {
                "success": False,
                "message": "Validation error.",
                "errors": exc.message_dict if hasattr(exc, "message_dict") else exc.messages,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Unhandled server errors — log and return 500
    logger.exception("Unhandled server error: %s", exc)
    return Response(
        {"success": False, "message": "Internal server error."},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def _extract_message(data) -> str:
    """Pull a human-readable string from DRF error data."""
    if isinstance(data, list) and data:
        first = data[0]
        return str(first) if not isinstance(first, dict) else "Validation error."
    if isinstance(data, dict):
        for key, value in data.items():
            if key == "detail":
                return str(value)
            if isinstance(value, list) and value:
                return f"{key}: {value[0]}"
        return "Validation error."
    return str(data)
