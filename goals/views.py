from django.db.models import Max, F

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

        # set order number and user for a new goal
        user = self.request.user
        order = self.request.data.get('order')

        if not order:
            max_order = Goal.objects.filter(user=user, active=True).aggregate(
                max=Max('order')
            ).get('max')
            order = max_order + 1 if max_order else 1
        serializer.save(user=user, order=order)

    def perform_destroy(self, instance):
        order = instance.order
        super().perform_destroy(instance)

        # update order or remaining objects
        (
            Goal.objects
            .filter(user=self.request.user)
            .filter(order__gt=order)
            .update(order=F('order')-1)
        )
