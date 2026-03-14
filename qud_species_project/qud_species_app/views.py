from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models.functions import Cast, Substr, StrIndex, Concat
from django.db.models import IntegerField, Value as V, Count, Avg, Max, Min
from django_filters.rest_framework import DjangoFilterBackend

from .models import Creature, Skill, Mutation, Anatomy, BodyPart
from .serializers import (
    CreatureSerializer, SkillSerializer, MutationSerializer, 
    AnatomySerializer, BodyPartSerializer
)
from .filters import CreatureFilter
from drf_spectacular.utils import extend_schema_view
from .schemas import CREATURE_SCHEMAS, SKILL_SCHEMAS, MUTATION_SCHEMAS, ANATOMY_SCHEMAS, BODY_PART_SCHEMAS

@extend_schema_view(
    list=CREATURE_SCHEMAS["list"],
    create=CREATURE_SCHEMAS["create"],
    retrieve=CREATURE_SCHEMAS["retrieve"],
    update=CREATURE_SCHEMAS["update"],
    partial_update=CREATURE_SCHEMAS["partial_update"],
    destroy=CREATURE_SCHEMAS["destroy"],
    summary_stats=CREATURE_SCHEMAS["summary_stats"],
    stat_averages_per_type=CREATURE_SCHEMAS["stat_averages_per_type"],
)
class CreatureViewSet(viewsets.ModelViewSet):
    # Sorting attributes so they can be ordered, can contain dice values like 16,1d3
    attrs = ['strength', 'agility', 'toughness', 'intelligence', 'willpower', 'ego']
    annotations = {
        f"{a}_base": Cast(
            Substr(Concat(a, V(',')), 1, StrIndex(Concat(a, V(',')), V(',')) - 1),
            output_field=IntegerField()
        ) for a in attrs
    }
    
    queryset = Creature.objects.annotate(**annotations)
    serializer_class = CreatureSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = CreatureFilter
    
    # Added 'species' to ordering_fields
    ordering_fields = ['name', 'species', 'hitpoints', 'av', 'dv', 'level', 'type'] + [f"{a}_base" for a in attrs]
    ordering = ['name']

    @action(detail=False, methods=['get'])
    def summary_stats(self, request):
        #Returns the number of creatures associated with each category.
        data = {
            "by_species": Creature.objects.values('species').annotate(count=Count('id')).order_by('-count'),
            "by_mutation": Mutation.objects.annotate(count=Count('creature')).values('internal_name', 'count').order_by('-count'),
            "by_skill": Skill.objects.annotate(count=Count('creature')).values('internal_name', 'count').order_by('-count'),
            "by_anatomy": Anatomy.objects.annotate(count=Count('creature')).values('name', 'count').order_by('-count'),
        }
        return Response(data)

    @action(detail=False, methods=['get'])
    def stat_averages_per_type(self, request):
      
        # Returns average stats, ignoring 0s
        stats = Creature.objects.filter(
            hitpoints__gt=0, 
            level__gt=0
        ).values('type').annotate(
            avg_hp=Avg('hitpoints'),
            max_hp=Max('hitpoints'),
            avg_av=Avg('av'),
            avg_dv=Avg('dv'),
            creature_count=Count('id')
        ).order_by('type')
        
        return Response(stats)

@extend_schema_view(
    list=SKILL_SCHEMAS["list"],
    retrieve=SKILL_SCHEMAS["retrieve"],
    create=SKILL_SCHEMAS["create"],
    update=SKILL_SCHEMAS["update"],
    partial_update=SKILL_SCHEMAS["partial_update"],
    destroy=SKILL_SCHEMAS["destroy"],
    distribution=SKILL_SCHEMAS["distribution"],
)
class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

    @action(detail=False, methods=['get'])
    def distribution(self, request):
        stats = Skill.objects.annotate(count=Count('creature')).order_by('-count')
        data = [{"skill": s.internal_name, "creature_count": s.count} for s in stats]
        return Response(data)

@extend_schema_view(
    list=MUTATION_SCHEMAS["list"],
    retrieve=MUTATION_SCHEMAS["retrieve"],
    create=MUTATION_SCHEMAS["create"],
    update=MUTATION_SCHEMAS["update"],
    partial_update=MUTATION_SCHEMAS["partial_update"],
    destroy=MUTATION_SCHEMAS["destroy"],
    distribution=MUTATION_SCHEMAS["distribution"],
)
class MutationViewSet(viewsets.ModelViewSet):
    queryset = Mutation.objects.all()
    serializer_class = MutationSerializer

    @action(detail=False, methods=['get'])
    def distribution(self, request):
        stats = Mutation.objects.annotate(count=Count('creature')).order_by('-count')
        data = [{"mutation": m.internal_name, "creature_count": m.count} for m in stats]
        return Response(data)

@extend_schema_view(
    list=ANATOMY_SCHEMAS["list"],
    retrieve=ANATOMY_SCHEMAS["retrieve"],
    create=ANATOMY_SCHEMAS["create"],
    update=ANATOMY_SCHEMAS["update"],
    partial_update=ANATOMY_SCHEMAS["partial_update"],
    destroy=ANATOMY_SCHEMAS["destroy"],
    distribution=ANATOMY_SCHEMAS["distribution"],
)
class AnatomyViewSet(viewsets.ModelViewSet):
    queryset = Anatomy.objects.all()
    serializer_class = AnatomySerializer

    @action(detail=False, methods=['get'])
    def distribution(self, request):
        stats = Anatomy.objects.annotate(count=Count('creature')).order_by('-count')
        data = [{"anatomy_name": a.name, "creature_count": a.count} for a in stats]
        return Response(data)

@extend_schema_view(
    list=BODY_PART_SCHEMAS["list"],
    retrieve=BODY_PART_SCHEMAS["retrieve"],
    create=BODY_PART_SCHEMAS["create"],
    update=BODY_PART_SCHEMAS["update"],
    partial_update=BODY_PART_SCHEMAS["partial_update"],
    destroy=BODY_PART_SCHEMAS["destroy"],
)
class BodyPartViewSet(viewsets.ModelViewSet):
    queryset = BodyPart.objects.all()
    serializer_class = BodyPartSerializer