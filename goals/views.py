from django.db.models import Max

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import GoalSerializer
from .models import Goal


class GoalsViewSet(viewsets.ModelViewSet):
    """
    Goals viewset for listing, creating and managing Goals, Wallets and Pockets
    """

    serializer_class = GoalSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """get current users goals"""
        return Goal.objects.filter(
            user=self.request.user,
            active=True
        ).order_by('order')

    def perform_create(self, serializer):
        """
        create new goal wallet or pocket for current user assign order to it
        """

        # save a goal
        user = self.request.user
        max_order = Goal.objects.filter(user=user, active=True).aggregate(
            max=Max('order')
        ).get('max')
        new_obj_order = max_order + 1 if max_order else 1
        serializer.save(user=user, order=new_obj_order)
