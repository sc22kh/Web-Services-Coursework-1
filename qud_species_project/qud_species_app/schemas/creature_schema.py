from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiTypes
from ..serializers import CreatureSerializer
from ..models import Creature
from .shared_error_examples import AUTH_ERROR_EXAMPLES

# Example Data
APOTHECARY_DATA = {
    "id": 1229,
    "name": "Apothecary",
    "type": "merchants",
    "av": 3,
    "dv": 0,
    "hitpoints": 70,
    "level": "18-20",
    "strength": "14,1d3,(t)d1",
    "agility": "14,1d3,(t)d1",
    "toughness": "14,1d3,(t)d1",
    "intelligence": "14,1d3,(t)d1",
    "willpower": "14,1d3,(t)d1",
    "ego": "14,1d3,(t)d1",
    "heat_resistance": 0,
    "cold_resistance": 0,
    "electric_resistance": 0,
    "acid_resistance": 0,
    "species": "human",
    "faction": "Merchants",
    "anatomy": 1,
    "mutations": [],
    "skills": [22, 49, 50, 52]
}

CREATURE_SCHEMAS = {
    "list": extend_schema(
        summary="Retrieve all creatures",
        description="Returns a detailed list of all creatures.",
        parameters=[
            OpenApiParameter(name='mutations', type=str, description='Filter by mutation internal_name'),
            OpenApiParameter(name='skills', type=str, description='Filter by skill internal_name'),
            OpenApiParameter(name='anatomy', type=str, description='Filter by anatomy name'),
            OpenApiParameter(name='type', enum=[choice[0] for choice in Creature.TYPE_CHOICES]),
            OpenApiParameter(name='species', type=str),
            OpenApiParameter(name='ordering', type=str, enum=[
                'name', '-name', 'species', '-species', 'hitpoints', '-hitpoints', 
                'av', '-av', 'dv', '-dv', 'level', '-level'
            ]),
            OpenApiParameter(name='part_name', type=str),
            OpenApiParameter(name='part_count_min', type=int),
        ],
        examples=[
            OpenApiExample("Apothecary in list", value=[APOTHECARY_DATA])
        ],
        responses={200: CreatureSerializer}
    ),

    "create": extend_schema(
        summary="Create a new creature",
        examples=[
            OpenApiExample("Apothecary Request", value={
                "name": "Apothecary",
                "type": "merchants",
                "av": 3,
                "dv": 0,
                "hitpoints": 70,
                "level": "18-20",
                "strength": "14,1d3,(t)d1",
                "agility": "14,1d3,(t)d1",
                "toughness": "14,1d3,(t)d1",
                "intelligence": "14,1d3,(t)d1",
                "willpower": "14,1d3,(t)d1",
                "ego": "14,1d3,(t)d1",
                "heat_resistance": 0,
                "cold_resistance": 0,
                "electric_resistance": 0,
                "acid_resistance": 0,
                "species": "human",
                "faction": "Merchants",
                "anatomy": 1,
                "mutations": [],
                "skills": [22, 49, 50, 52]
            }, request_only=True),
            OpenApiExample("Apothecary Response", value=APOTHECARY_DATA, response_only=True),
            *AUTH_ERROR_EXAMPLES,
            OpenApiExample('Validation Error', status_codes=["400"], value={"name": ["This field is required."]})
        ],
        responses={201: CreatureSerializer, 400: OpenApiTypes.OBJECT, 401: OpenApiTypes.OBJECT, 403: OpenApiTypes.OBJECT}
    ),

    "retrieve": extend_schema(
        summary="Retrieve creature by ID",
        description="Returns detailed information about a specific creature by ID.",
        examples=[
            OpenApiExample("Apothecary", value=APOTHECARY_DATA),
            OpenApiExample('Not Found', status_codes=["404"], value={"detail": "No Creature matches the given query."})
        ],
        responses={200: CreatureSerializer, 404: OpenApiTypes.OBJECT}
    ),

    "update": extend_schema(
        summary="Update a creature",
        examples=[
            OpenApiExample("Apothecary Example", value=APOTHECARY_DATA),
            *AUTH_ERROR_EXAMPLES,
            OpenApiExample('Not Found', status_codes=["404"], value={"detail": "No Creature matches the given query."}),
            OpenApiExample('Validation Error', status_codes=["400"], value={"name": ["This field is required."]})
        ],
        responses={200: CreatureSerializer, 400: OpenApiTypes.OBJECT, 401: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT}
    ),

    "partial_update": extend_schema(
        summary="Partially update a creature",
        examples=[
            OpenApiExample("Patch HP", value={"hitpoints": 75}),
            OpenApiExample('Invalid Data', status_codes=["400"], value={"hitpoints": ["A valid integer is required."]}),
            *AUTH_ERROR_EXAMPLES
        ],
        responses={200: CreatureSerializer, 400: OpenApiTypes.OBJECT, 401: OpenApiTypes.OBJECT}
    ),

    "destroy": extend_schema(
        summary="Delete a creature",
        examples=[
            OpenApiExample("Deleted", status_codes=["204"], value=None),
            OpenApiExample('Not Found', status_codes=["404"], value={"detail": "No Creature matches the given query."}),
            *AUTH_ERROR_EXAMPLES
        ],
        responses={204: None, 401: OpenApiTypes.OBJECT, 403: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT}
    ),

    "summary_stats": extend_schema(
        summary="Creature distribution statistics",
        responses={200: OpenApiTypes.OBJECT},
        examples=[
            OpenApiExample("Summary Stats", value={
                "by_species": [{"species": "human", "count": 199}],
                "by_anatomy": [{"name": "Humanoid", "count": 377}]
            })
        ]
    ),

    "stat_averages_per_type": extend_schema(
        summary="Average stats by type",
        responses={200: OpenApiTypes.OBJECT},
        examples=[
            OpenApiExample("Averages", value=[{
                "type": "merchants",
                "avg_hp": 119.25,
                "max_hp": 295,
                "avg_av": 2.9166666666666665,
                "avg_dv": 0.0,
                "creature_count": 60
            },])
        ]
    ),
}