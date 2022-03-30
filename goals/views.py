from django.db.models import Max, F

from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Goal, Wallet, Pocket
from .serializers import GoalSerializer, WalletSerializer


class GoalsViewSet(viewsets.ModelViewSet):
    """
    Goals viewset for listing, creating and managing Goals
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = GoalSerializer

    def get_queryset(self):
        """get current users goals"""
        return Goal.objects.filter(
            user=self.request.user,
            active=True
        ).order_by('order')

    def perform_create(self, serializer):
        """
        create new goal for current user assign order to it
        """

        # set order number and user for a new goal
        user = self.request.user

        max_order = Goal.objects.filter(user=user, active=True).aggregate(
            max=Max('order')
        ).get('max')
        order = max_order + 1 if max_order else 1

        serializer.save(user=user, order=order)

    def perform_destroy(self, instance):
        order = instance.order
        super().perform_destroy(instance)

        # update order for remaining objects
        (
            Goal.objects
            .filter(user=self.request.user)
            .filter(order__gt=order)
            .update(order=F('order')-1)
        )


class WalletViewSet(viewsets.GenericViewSet,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.RetrieveModelMixin):
    """
    Wallet viewset for listing, creating and managing Wallets
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = WalletSerializer

    def get_queryset(self):
        """Get current users wallets"""
        goal_ids = Goal.objects.filter(user=self.request.user).values('id')

        return Wallet.objects.filter(
            goal__id__in=goal_ids,
            active=True
        ).order_by('order')

    def perform_create(self, serializer):
        """
        create new wallet for specified goal and assign order to it
        """

        # set order number and goal for a new wallet
        goal = Goal.objects.get(pk=self.request.data['goal'])

        max_order = (
            Wallet.objects.filter(active=True, goal=goal)
            .aggregate(max=Max('order'))
            .get('max')
        )
        order = max_order + 1 if max_order else 1

        serializer.save(goal=goal, order=order)

    def perform_destroy(self, instance):
        order = instance.order
        super().perform_destroy(instance)

        # update order for remaining objects
        (
            Goal.objects
            .filter(user=self.request.user)
            .filter(order__gt=order)
            .update(order=F('order')-1)
        )
