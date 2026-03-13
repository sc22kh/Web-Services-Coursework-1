from rest_framework import viewsets

from django_filters.rest_framework import DjangoFilterBackend
from .models import Creature, Skill, Mutation, Anatomy, BodyPart
from .serializers import CreatureSerializer, SkillSerializer, MutationSerializer, AnatomySerializer, BodyPartSerializer
from .filters import CreatureFilter

class CreatureViewSet(viewsets.ModelViewSet):
    queryset = Creature.objects.all()
    serializer_class = CreatureSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CreatureFilter

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