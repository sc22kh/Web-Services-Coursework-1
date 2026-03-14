from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiTypes
from ..serializers import MutationSerializer
from .shared_error_examples import AUTH_ERROR_EXAMPLES

# Example Data
CHIMERA_DATA = {
    "id": 1,
    "name": "Chimera",
    "internal_name": "Chimera",
    "cost": 1,
    "type": "morphotypes"
}

MUTATION_SCHEMAS = {
    "list": extend_schema(
        summary="Retrieve all mutations",
        responses={200: MutationSerializer},
        examples=[
            OpenApiExample("Mutation List Example", value=[CHIMERA_DATA], response_only=True)
        ]
    ),

    "retrieve": extend_schema(
        summary="Retrieve mutation by ID",
        responses={200: MutationSerializer, 404: OpenApiTypes.OBJECT},
        examples=[
            OpenApiExample("Mutation Detail", value=CHIMERA_DATA, response_only=True),
            OpenApiExample("Not Found", status_codes=["404"], value={"detail": "No Mutation matches..."})
        ]
    ),

    "create": extend_schema(
        summary="Create mutation",
        responses={201: MutationSerializer, 400: OpenApiTypes.OBJECT, 401: OpenApiTypes.OBJECT, 403: OpenApiTypes.OBJECT},
        examples=[
            OpenApiExample("Create Request", value=CHIMERA_DATA, request_only=True),
            OpenApiExample("Create Response", value=CHIMERA_DATA, status_codes=["201"], response_only=True),
            *AUTH_ERROR_EXAMPLES,
            OpenApiExample("Validation Error", status_codes=["400"], value={"internal_name": ["Required."], "type": ["Invalid choice."]})
        ]
    ),

    "update": extend_schema(
        summary="Update mutation",
        responses={200: MutationSerializer, 400: OpenApiTypes.OBJECT, 401: OpenApiTypes.OBJECT, 403: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT},
        examples=[
            OpenApiExample("Full Update Example", value={**CHIMERA_DATA, "cost": 2}, response_only=True),
            *AUTH_ERROR_EXAMPLES,
            OpenApiExample("Not Found", status_codes=["404"], value={"detail": "No Mutation matches..."})
        ]
    ),

    "partial_update": extend_schema(
        summary="Partial update mutation",
        responses={200: MutationSerializer, 400: OpenApiTypes.OBJECT, 401: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT},
        examples=[
            OpenApiExample("Patch Cost Example", value={"cost": 4}, response_only=True),
            *AUTH_ERROR_EXAMPLES
        ]
    ),

    "destroy": extend_schema(
        summary="Delete mutation",
        responses={204: None, 401: OpenApiTypes.OBJECT, 403: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT},
        examples=[
            OpenApiExample("Deleted", status_codes=["204"], value=None),
            *AUTH_ERROR_EXAMPLES
        ]
    ),

    "distribution": extend_schema(
        summary="Mutation distribution",
        responses={200: OpenApiTypes.OBJECT},
        examples=[
            OpenApiExample("Distribution Example", value=[
                {"mutation": "LiquidFont", "creature_count": 30},
                {"mutation": "DarkVision", "creature_count": 19}
            ], response_only=True)
        ]
    ),
}