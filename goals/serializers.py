from rest_framework import serializers

from .models import Goal, Wallet, Pocket


class PocketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pocket
        fields = '__all__'
        read_only_fields = ('order')

    def validate_percent_of_wallet(self, value):
        if value < 0:
            raise serializers.ValidationError('value must be positive')
        return value

    def validate_default_amount(self, value):
        if value < 0:
            raise serializers.ValidationError('value must be positive')
        return value

    def validate_wallet(self, value):
        wallet = Wallet.objects.filter(active=True).get(pk=value)
        if not wallet:
            raise serializers.ValidationError(
                'please, select an active valid Wallet')


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'
        read_only_fields = ('order')

    pockets = PocketSerializer(many=True, read_only=True)

    def validate_percent_of_goal(self, value):
        if value < 0:
            raise serializers.ValidationError('value must be positive')
        return value

    def validate_default_amount(self, value):
        if value < 0:
            raise serializers.ValidationError('value must be positive')
        return value

    def validate_goal(self, value):
        goal = Goal.objects.filter(active=True).get(pk=value)
        if not goal:
            raise serializers.ValidationError(
                'please, select an active valid Goal')


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ('user', 'order')

    wallets = WalletSerializer(many=True, read_only=True)

    def validate_percent_of_net(self, value):
        if value < 0:
            raise serializers.ValidationError('value must be positive')
        return value

    def validate_default_amount(self, value):
        if value < 0:
            raise serializers.ValidationError('value must be positive')
        return value
