from rest_framework import serializers

from .models import Goal, Wallet, Pocket


class PocketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pocket
        fields = '__all__'


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'

    pockets = PocketSerializer(many=True, read_only=True)


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ('user',)

    wallets = WalletSerializer(many=True, read_only=True)
