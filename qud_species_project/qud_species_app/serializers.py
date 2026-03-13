from rest_framework import serializers
from .models import Creature, Skill, Mutation, Anatomy, BodyPart

class CreatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creature
        fields = '__all__'

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"

class MutationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mutation
        fields = "__all__"

class AnatomySerializer(serializers.ModelSerializer):
    class Meta:
        model = Anatomy
        fields = "__all__"

class BodyPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = BodyPart
        fields = "__all__"