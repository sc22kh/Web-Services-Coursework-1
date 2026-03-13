import django_filters
from .models import Creature

class CreatureFilter(django_filters.FilterSet):
    # Filter by related field internal_name
    skills = django_filters.CharFilter(field_name="skills__internal_name", lookup_expr='icontains', label="Skills")
    mutations = django_filters.CharFilter(field_name="mutations__internal_name", lookup_expr='icontains',  label="Mutations")
    body_parts = django_filters.CharFilter(field_name="anatomy__parts__part_name", lookup_expr='icontains', label="Body Parts")    
    anatomy = django_filters.CharFilter(field_name="anatomy__name", lookup_expr='icontains',  label="Anatomies")

    class Meta:
        model = Creature
        fields = ['skills', 'mutations', 'body_parts', 'anatomy']