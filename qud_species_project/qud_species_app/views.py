from rest_framework import viewsets
from .models import Creature, Skill, Mutation, Anatomy, BodyPart
from .serializers import CreatureSerializer, SkillSerializer, MutationSerializer, AnatomySerializer, BodyPartSerializer

class CreatureViewSet(viewsets.ModelViewSet):
    queryset = Creature.objects.all()
    serializer_class = CreatureSerializer

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