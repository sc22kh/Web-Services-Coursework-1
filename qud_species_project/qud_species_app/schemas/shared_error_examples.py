from drf_spectacular.utils import OpenApiExample

# Common Error Examples
AUTH_ERROR_EXAMPLES = [
    OpenApiExample(
        'No Credentials',
        status_codes=["401"],
        value={"detail": "Authentication credentials were not provided."},
        response_only=True,
    ),
    OpenApiExample(
        'Forbidden',
        value={"detail": "You do not have permission to perform this action."},
        status_codes=["403"],
        response_only=True,
    ),
]