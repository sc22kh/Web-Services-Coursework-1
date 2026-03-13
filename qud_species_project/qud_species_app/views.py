from rest_framework import viewsets
from .models import Creature
from .serializers import CreatureSerializer

class CreatureViewSet(viewsets.ModelViewSet):
    queryset = Creature.objects.all()
    serializer_class = CreatureSerializer