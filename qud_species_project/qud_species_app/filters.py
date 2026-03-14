import django_filters
from django.db.models import Sum
from .models import Creature

class CreatureFilter(django_filters.FilterSet):
    type = django_filters.ChoiceFilter(choices=Creature.TYPE_CHOICES)
    species = django_filters.CharFilter(field_name="species", lookup_expr='icontains', label="Species")
    skill = django_filters.CharFilter(field_name="skills__internal_name", lookup_expr='icontains', label="Skill")
    mutation = django_filters.CharFilter(field_name="mutations__internal_name", lookup_expr='icontains',  label="Mutation")
    anatomy = django_filters.CharFilter(field_name="anatomy__name", lookup_expr='icontains',  label="Anatomy")

    part_count_min = django_filters.NumberFilter(method='filter_by_part_count', label="Minimum Number of BodyParts")
    part_name = django_filters.CharFilter(field_name="anatomy__parts__part_name", lookup_expr='icontains', label="for BodyPart Name")

    class Meta:
        model = Creature
        fields = ['type', 'species', 'skill', 'mutation', 'anatomy', 'part_count_min', 'part_name']

    def filter_by_part_count(self, queryset, name, value):
        #Filters creatures that have at least 'value' of a specific body part.
        #Requires 'part_name' to be provided in the query as well.
        return queryset.annotate(
            total_part_count=Sum('anatomy__bodypartcount__count')
        ).filter(total_part_count__gte=value)