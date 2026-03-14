from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiTypes
from ..serializers import BodyPartSerializer
from .shared_error_examples import AUTH_ERROR_EXAMPLES

# Example Data
LIP_DATA = {
    "id": 45,
    "part_name": "Lip",
    "integral": False,
    "appendage": True,
    "plural": False,
    "mortal": False,
    "usually_on": 2,
    "requires_part": 3
}

BODY_PART_SCHEMAS = {
    "list": extend_schema(
        summary="Retrieve all body parts",
        responses={200: BodyPartSerializer},
        examples=[
            OpenApiExample("Body Part List Example", value=[LIP_DATA], response_only=True)
        ]
    ),

    "retrieve": extend_schema(
        summary="Retrieve body part by ID",
        responses={200: BodyPartSerializer, 404: OpenApiTypes.OBJECT},
        examples=[
            OpenApiExample("Body Part Detail", value=LIP_DATA, response_only=True),
            OpenApiExample("Not Found", status_codes=["404"], value={"detail": "No BodyPart matches..."})
        ]
    ),

    "create": extend_schema(
        summary="Create body part",
        responses={201: BodyPartSerializer, 400: OpenApiTypes.OBJECT, 401: OpenApiTypes.OBJECT, 403: OpenApiTypes.OBJECT},
        examples=[
            OpenApiExample("Create Request", value=LIP_DATA, request_only=True),
            OpenApiExample("Create Response", value=LIP_DATA, status_codes=["201"], response_only=True),
            *AUTH_ERROR_EXAMPLES,
            OpenApiExample("Validation Error", status_codes=["400"], value={
                "part_name": ["This field is required."],
                "usually_on": ["Invalid pk \"99\" - object does not exist."]
            })
        ]
    ),

    "update": extend_schema(
        summary="Update body part",
        responses={200: BodyPartSerializer, 400: OpenApiTypes.OBJECT, 401: OpenApiTypes.OBJECT, 403: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT},
        examples=[
            OpenApiExample("Full Update Example", value={**LIP_DATA, "part_name": "Lower Lip"}, response_only=True),
            *AUTH_ERROR_EXAMPLES,
            OpenApiExample("Validation Error", status_codes=["400"], value={"part_name": ["This field is required."]})
        ]
    ),

    "partial_update": extend_schema(
        summary="Partial update body part",
        responses={200: BodyPartSerializer, 400: OpenApiTypes.OBJECT, 401: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT},
        examples=[
            OpenApiExample("Patch Mortal Example", value={"mortal": True}, response_only=True),
            *AUTH_ERROR_EXAMPLES,
            OpenApiExample("Invalid Type", status_codes=["400"], value={"mortal": ["Must be a valid boolean."]})
        ]
    ),

    "destroy": extend_schema(
        summary="Delete body part",
        responses={204: None, 401: OpenApiTypes.OBJECT, 403: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT},
        examples=[
            OpenApiExample("Deleted", status_codes=["204"], value=None),
            *AUTH_ERROR_EXAMPLES
        ]
    ),
}