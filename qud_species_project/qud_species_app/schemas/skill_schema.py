from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiTypes
from ..serializers import SkillSerializer 
from .shared_error_examples import AUTH_ERROR_EXAMPLES


# Example Data
SKILL_DATA = {
    "id": 1,
    "skilltree": "acrobatics",
    "name": "Swift Reflexes",
    "internal_name": "Acrobatics_SwiftReflexes",
    "cost": 0,
    "attribute": "agility"
}

SKILL_SCHEMAS = {
    "list": extend_schema(
        summary="Retrieve all skills",
        responses={200: SkillSerializer},
        examples=[OpenApiExample("Skill List Example", value=[SKILL_DATA], response_only=True)]
    ),
    
    "retrieve": extend_schema(
        summary="Retrieve skill by ID",
        responses={200: SkillSerializer, 404: OpenApiTypes.OBJECT},
        examples=[
            OpenApiExample("Skill Detail", value=SKILL_DATA, response_only=True),
            OpenApiExample("Not Found", status_codes=["404"], value={"detail": "No Skill matches..."})
        ]
    ),

    "create": extend_schema(
        summary="Create a new skill",
        request=SkillSerializer,
        responses={201: SkillSerializer, 400: OpenApiTypes.OBJECT, 401: OpenApiTypes.OBJECT, 403: OpenApiTypes.OBJECT},
        examples=[
            OpenApiExample("Create Request", value=SKILL_DATA, request_only=True),
            OpenApiExample("Create Response", value=SKILL_DATA, status_codes=["201"], response_only=True),
            *AUTH_ERROR_EXAMPLES, # Reusing the list we made for Creatures!
            OpenApiExample("Validation Error", status_codes=["400"], value={"internal_name": ["Required."]})
        ]
    ),

    "update": extend_schema(
        summary="Update a skill",
        responses={200: SkillSerializer, 400: OpenApiTypes.OBJECT, 401: OpenApiTypes.OBJECT, 403: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT},
        examples=[
            OpenApiExample("Full Update", value={**SKILL_DATA, "cost": 50}, response_only=True),
            *AUTH_ERROR_EXAMPLES
        ]
    ),

    "partial_update": extend_schema(
        summary="Partially update a skill",
        responses={200: SkillSerializer, 400: OpenApiTypes.OBJECT, 401: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT},
        examples=[OpenApiExample("Patch Cost", value={"cost": 100}, response_only=True)]
    ),

    "destroy": extend_schema(
        summary="Delete a skill",
        responses={204: None, 401: OpenApiTypes.OBJECT, 403: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT},
        examples=[OpenApiExample("Deleted", status_codes=["204"], value=None)]
    ),

    "distribution": extend_schema(
        summary="Skill distribution across creatures",
        responses={200: OpenApiTypes.OBJECT},
        examples=[
            OpenApiExample("Distribution Example", value=[
                {"skill": "Tinkering_Tinker1", "creature_count": 28}
            ], response_only=True)
        ]
    ),
}