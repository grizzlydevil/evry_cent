from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Cycle, Income
from .serializers import CycleSerializer, IncomeSerializer


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
