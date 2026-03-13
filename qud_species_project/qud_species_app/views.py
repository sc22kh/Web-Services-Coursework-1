from rest_framework import viewsets, filters
from django.db.models.functions import Cast, Substr, StrIndex, Concat
from django.db.models import IntegerField, Value as V
from django_filters.rest_framework import DjangoFilterBackend
from .models import Creature, Skill, Mutation, Anatomy, BodyPart
from .serializers import CreatureSerializer, SkillSerializer, MutationSerializer, AnatomySerializer, BodyPartSerializer
from .filters import CreatureFilter

class CreatureViewSet(viewsets.ModelViewSet):
    # Sorting attributes so they can be ordered, can contain dice values like 1d3
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
    ordering_fields = ['name', 'hitpoints', 'av', 'dv', 'level', 'type'] + [f"{a}_base" for a in attrs]
    ordering = ['name']

class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

class MutationViewSet(viewsets.ModelViewSet):
    queryset = Mutation.objects.all()
    serializer_class = MutationSerializer

class AnatomyViewSet(viewsets.ModelViewSet):
    queryset = Anatomy.objects.all()
    serializer_class = AnatomySerializer

class BodyPartViewSet(viewsets.ModelViewSet):
    queryset = BodyPart.objects.all()
    serializer_class = BodyPartSerializer