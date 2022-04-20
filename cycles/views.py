from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Cycle, Income, IncomeDistributor
from .serializers import (CycleSerializer, IncomeSerializer,
                          IncomeDistributorSerializer)


class CycleViewSet(viewsets.ModelViewSet):
    """CRUD Cycle"""

    permission_classes = (IsAuthenticated,)
    serializer_class = CycleSerializer

    def get_queryset(self):
        """get current users cycles"""
        return Cycle.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """add current user to serializer"""
        serializer.save(user=self.request.user)


class IncomeViewSet(viewsets.ModelViewSet):
    """CRUD incomes"""

    permission_classes = (IsAuthenticated,)
    serializer_class = IncomeSerializer

    def get_queryset(self):
        """get current users incomes"""
        return Income.objects.filter(cycle__user=self.request.user)


class IncomeDistributorViewSet(viewsets.ModelViewSet):
    """List view will list all distributors with specified range of cycles"""

    permission_classes = (IsAuthenticated,)
    serializer_class = IncomeDistributorSerializer

    def get_queryset(self):
        """list only the items in specified cycles"""
        distributors = (IncomeDistributor.objects
                        .filter(cycle__user=self.request.user))
        if self.action == 'list':
            cycles_params = self.request.query_params.get('cycles')
            cycles = (
                [pk for pk in cycles_params.split(',') if pk.isdigit()]
                if cycles_params else []
            )
            distributors = (
                IncomeDistributor.objects
                .filter(cycle__in=cycles)
            )

        return distributors
