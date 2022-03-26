from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import GoalSerializer
from .models import Goal


class ListGoalsView(generics.ListAPIView):
    """
    List all Goals, Wallets and Pockets
    """

    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(
            user=self.request.user
        ).order_by('order')
