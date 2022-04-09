from rest_framework import serializers

from .models import Goal, Wallet, Pocket


class FieldValuesFilteredByUser(serializers.PrimaryKeyRelatedField):
    """
    This class filters foreign key to current user and active field values only
    """
    def get_queryset(self):
        user = self.context['request'].user
        if self.field_name == 'wallet':
            field_values = Wallet.objects.filter(goal__user=user)
        elif self.field_name == 'goal':
            field_values = Goal.objects.filter(user=user)

        field_values.filter(active=True)

        return field_values


class PocketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pocket
        fields = '__all__'
        read_only_fields = ('order',)

    active = serializers.BooleanField(initial=True)
    wallet = FieldValuesFilteredByUser()

    def validate_percent_of_wallet(self, value):
        if value and value < 0:
            raise serializers.ValidationError('value must be positive')
        return value

    def validate_default_amount(self, value):
        if value and value < 0:
            raise serializers.ValidationError('value must be positive')
        return value

    def validate_save_target(self, value):
        if value and value < 0:
            raise serializers.ValidationError('value must be positive')
        return value

    def validate_wallet(self, value):
        if (
            value.goal.user != self.context['request'].user or
            not value.active
        ):
            raise serializers.ValidationError(
                'please, select an active valid Wallet')

        return value


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'
        read_only_fields = ('order',)

    pockets = PocketSerializer(many=True, read_only=True)

    active = serializers.BooleanField(initial=True)
    goal = FieldValuesFilteredByUser()

    def validate_percent_of_goal(self, value):
        if value and value < 0:
            raise serializers.ValidationError('value must be positive')
        return value

    def validate_default_amount(self, value):
        if value and value < 0:
            raise serializers.ValidationError('value must be positive')
        return value

    def validate_goal(self, value):
        if (
            value.user != self.context['request'].user or
            not value.active
        ):
            raise serializers.ValidationError(
                'please, select an active valid Goal')

        return value


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ('user', 'order')

    wallets = WalletSerializer(many=True, read_only=True)

    active = serializers.BooleanField(initial=True)

    def validate_percent_of_net(self, value):
        if value and value < 0:
            raise serializers.ValidationError('value must be positive')
        return value

    def validate_default_amount(self, value):
        if value and value < 0:
            raise serializers.ValidationError('value must be positive')
        return value
