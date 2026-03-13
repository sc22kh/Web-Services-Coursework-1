from django.contrib import admin
from .models import Creature, Mutation, Anatomy, BodyPart, BodyPartCount, Skill

admin.site.register(Creature)
admin.site.register(Mutation)
admin.site.register(Anatomy)
admin.site.register(BodyPart)
admin.site.register(BodyPartCount)
admin.site.register(Skill)
