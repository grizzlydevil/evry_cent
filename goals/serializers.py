from django.db.models import F

from rest_framework import serializers

from .models import Goal, Wallet, Pocket, PocketGroup


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


class PocketGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = PocketGroup
        fields = ('title', 'pockets')

    # pockets = serializers.ListField(
    #     child=serializers.IntegerField(min_value=0),
    #     min_length=1,
    #     max_length=10
    # )

    def validate_pockets(self, value):
        pass
        # validate all id in the list are unique
        if len(value) != len(set(value)):
            raise serializers.ValidationError(
                'dublicate pockets are not possible')

        pocket_ids = (pocket.id for pocket in value)
        selected_pockets = Pocket.objects.filter(id__in=pocket_ids)

        # validate pockets are active
        if selected_pockets.filter(active=False).exists():
            raise serializers.ValidationError('all pockets must be active')

        # validate pockets belong to this user
        if selected_pockets.exclude(
            wallet__goal__user=self.context['request'].user
        ).exists():
            raise serializers.ValidationError('invalid pockets selected')

        # validate no pockets in the list are in other pocket groups
        pockets_in_other_groups = selected_pockets.filter(
            pocket_group__isnull=False)
        if pockets_in_other_groups.exists():
            titles = (
                f'"{pocket.title}"' for pocket in pockets_in_other_groups
            )
            raise serializers.ValidationError(
                f'pockets: {", ".join(titles)} belong to other groups already'
            )

        # # add pocket_group Id to selected pockets
        # selected_pockets.update(pocket_group=self.id)
