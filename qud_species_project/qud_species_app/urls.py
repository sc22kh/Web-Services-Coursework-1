from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CreatureViewSet,  SkillViewSet, MutationViewSet, AnatomyViewSet, BodyPartViewSet

router = DefaultRouter()
router.register(r'creatures', CreatureViewSet)
router.register(r'skills', SkillViewSet)
router.register(r'mutations', MutationViewSet)
router.register(r'anatomies', AnatomyViewSet)
router.register(r'body-parts', BodyPartViewSet)

urlpatterns = [
    path('', include(router.urls)),
]