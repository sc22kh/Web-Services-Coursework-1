from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiTypes
from ..serializers import AnatomySerializer
from .shared_error_examples import AUTH_ERROR_EXAMPLES

# Example Data
HUMANOID_DATA = {
    "id": 1,
    "name": "Humanoid",
    "parts": [2, 3, 4, 5, 6, 8, 9, 12]
}

ANATOMY_SCHEMAS = {
    "list": extend_schema(
        summary="Retrieve all anatomies",
        responses={200: AnatomySerializer},
        examples=[
            OpenApiExample("Anatomy List Example", value=[HUMANOID_DATA], response_only=True)
        ]
    ),

    "retrieve": extend_schema(
        summary="Retrieve anatomy by ID",
        responses={200: AnatomySerializer, 404: OpenApiTypes.OBJECT},
        examples=[
            OpenApiExample("Anatomy Detail", value=HUMANOID_DATA, response_only=True),
            OpenApiExample("Not Found", status_codes=["404"], value={"detail": "No Anatomy matches..."})
        ]
    ),

    "create": extend_schema(
        summary="Create anatomy",
        responses={201: AnatomySerializer, 400: OpenApiTypes.OBJECT, 401: OpenApiTypes.OBJECT, 403: OpenApiTypes.OBJECT},
        examples=[
            OpenApiExample("Create Request", value=HUMANOID_DATA, request_only=True),
            OpenApiExample("Create Response", value=HUMANOID_DATA, status_codes=["201"], response_only=True),
            *AUTH_ERROR_EXAMPLES,
            OpenApiExample("Validation Error", status_codes=["400"], value={
                "part_name": ["body part with this part name already exists."],
                "usually_on": ["Invalid pk \"9999\" - object does not exist."]
            })
        ]
    ),

    "update": extend_schema(
        summary="Update anatomy",
        responses={200: AnatomySerializer, 400: OpenApiTypes.OBJECT, 401: OpenApiTypes.OBJECT, 403: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT},
        examples=[
            OpenApiExample("Full Update Example", value={**HUMANOID_DATA, "name": "Modified Humanoid"}, response_only=True),
            *AUTH_ERROR_EXAMPLES,
            OpenApiExample("Validation Error", status_codes=["400"], value={"parts": ["Invalid pk \"999\" - object does not exist."]})
        ]
    ),

    "partial_update": extend_schema(
        summary="Partial update anatomy",
        responses={200: AnatomySerializer, 400: OpenApiTypes.OBJECT, 401: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT},
        examples=[
            OpenApiExample("Patch Parts Example", value={"parts": [1, 2, 3]}, response_only=True),
            *AUTH_ERROR_EXAMPLES,
            OpenApiExample("Invalid Data", status_codes=["400"], value={"parts": ["Expected a list of items but got type \"string\"."]})
        ]
    ),

    "destroy": extend_schema(
        summary="Delete anatomy",
        responses={204: None, 401: OpenApiTypes.OBJECT, 403: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT},
        examples=[
            OpenApiExample("Deleted", status_codes=["204"], value=None),
            *AUTH_ERROR_EXAMPLES
        ]
    ),

    "distribution": extend_schema(
        summary="Anatomy distribution",
        responses={200: OpenApiTypes.OBJECT},
        examples=[
            OpenApiExample("Anatomy Dist Example", value=[
                {"anatomy_name": "Humanoid", "creature_count": 377},
                {"anatomy_name": "Quadruped", "creature_count": 123}
            ], response_only=True)
        ]
    ),
}