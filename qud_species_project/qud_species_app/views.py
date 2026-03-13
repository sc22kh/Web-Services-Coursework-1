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
        """
        Returns the number of creatures associated with each category.
        """
        data = {
            "by_species": Creature.objects.values('species').annotate(count=Count('id')).order_by('-count'),
            "by_mutation": Mutation.objects.annotate(count=Count('creature')).values('internal_name', 'count').order_by('-count'),
            "by_skill": Skill.objects.annotate(count=Count('creature')).values('internal_name', 'count').order_by('-count'),
            "by_anatomy": Anatomy.objects.annotate(count=Count('creature')).values('name', 'count').order_by('-count'),
        }
        return Response(data)

    @action(detail=False, methods=['get'])
    def stat_averages_per_type(self, request):
        """
        Provides analytics on the 'Power Level' of creatures grouped by type.
        Filters out creatures with 0 hitpoints or level to ensure clean averages.
        """
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

class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

    @action(detail=False, methods=['get'])
    def distribution(self, request):
        stats = Skill.objects.annotate(count=Count('creature')).order_by('-count')
        data = [{"skill": s.internal_name, "creature_count": s.count} for s in stats]
        return Response(data)

class MutationViewSet(viewsets.ModelViewSet):
    queryset = Mutation.objects.all()
    serializer_class = MutationSerializer

    @action(detail=False, methods=['get'])
    def distribution(self, request):
        stats = Mutation.objects.annotate(count=Count('creature')).order_by('-count')
        data = [{"mutation": m.internal_name, "creature_count": m.count} for m in stats]
        return Response(data)

class AnatomyViewSet(viewsets.ModelViewSet):
    queryset = Anatomy.objects.all()
    serializer_class = AnatomySerializer

    @action(detail=False, methods=['get'])
    def distribution(self, request):
        stats = Anatomy.objects.annotate(count=Count('creature')).order_by('-count')
        data = [{"anatomy_name": a.name, "creature_count": a.count} for a in stats]
        return Response(data)

class BodyPartViewSet(viewsets.ModelViewSet):
    queryset = BodyPart.objects.all()
    serializer_class = BodyPartSerializer