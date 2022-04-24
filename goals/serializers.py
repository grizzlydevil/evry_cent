from django.db.models import Q

from rest_framework import serializers

from .models import Goal, Wallet, Pocket, PocketGroup
from banks.models import Account, Vault


class FieldValuesFilteredByUser(serializers.PrimaryKeyRelatedField):
    """
    This class filters foreign key to current user and active field values only
    """
    def get_queryset(self):
        user = self.context['request'].user
        if self.field_name == 'wallet':
            field_values = (
                Wallet.objects.filter(goal__user=user).filter(active=True)
            )
        elif self.field_name == 'goal':
            field_values = (
                Goal.objects.filter(user=user).filter(active=True)
            )
        elif self.parent.field_name == 'pockets':
            field_values = (
                Pocket.objects.filter(wallet__goal__user=user)
                .filter(active=True)
            )
        elif self.field_name == 'pocket_group':
            field_values = PocketGroup.objects.filter(user=user)
        elif self.field_name == 'account':
            field_values = Account.objects.filter(bank__user=user)
        elif self.field_name == 'vault':
            field_values = Vault.objects.filter(account__bank__user=user)

        return field_values


class PocketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pocket
        fields = '__all__'
        read_only_fields = ('order', 'active')

    wallet = FieldValuesFilteredByUser()
    pocket_group = FieldValuesFilteredByUser(required=False)
    account = FieldValuesFilteredByUser(required=False)
    vault = FieldValuesFilteredByUser(required=False)

    def validate_percent_of_wallet(self, value):
        if value and (value < 0 or value > 100):
            raise serializers.ValidationError(
                'value must be positive and no more than 100')
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
        read_only_fields = ('order', 'active')

    pockets = PocketSerializer(many=True, read_only=True)

    goal = FieldValuesFilteredByUser()

    def validate_percent_of_goal(self, value):
        if value and (value < 0 or value > 100):
            raise serializers.ValidationError(
                'value must be positive and no more than 100')
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
        read_only_fields = ('user', 'order', 'active')

    wallets = WalletSerializer(many=True, read_only=True)

    def validate_percent_of_net(self, value):
        if value and (value < 0 or value > 100):
            raise serializers.ValidationError(
                'value must be positive and no more than 100')
        return value

    def validate_default_amount(self, value):
        if value and value < 0:
            raise serializers.ValidationError('value must be positive')
        return value


class PocketGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = PocketGroup
        fields = ('title', 'pockets')

    pockets = serializers.ManyRelatedField(
        child_relation=FieldValuesFilteredByUser()
    )

    def validate_pockets(self, value):

        # validate at least one pocket was specified
        if len(value) < 1:
            raise serializers.ValidationError(
                'please specify at least one pocket'
            )

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
        if self.instance:
            # if instance exists means it's an update.
            # Pockets may exist in current instance
            group_id = self.instance.id
            pockets_in_other_groups = selected_pockets.filter(
                Q(pocket_group__isnull=False) & ~Q(pocket_group=group_id)
            )
        else:
            pockets_in_other_groups = selected_pockets.filter(
                pocket_group__isnull=False)

        if pockets_in_other_groups.exists():
            titles = (
                f'"{pocket.title}"' for pocket in pockets_in_other_groups
            )
            raise serializers.ValidationError(
                f'pockets: {", ".join(titles)} belong to other groups already'
            )

        return value

    def create(self, validated_data):
        """Selected pockets must be assigned to a newly created group"""
        pockets = validated_data.pop('pockets')
        pocket_ids = (pocket.id for pocket in pockets)
        selected_pockets = Pocket.objects.filter(id__in=pocket_ids)

        pocket_group = PocketGroup.objects.create(**validated_data)

        # add pocket_group Id to selected pockets
        selected_pockets.update(pocket_group=pocket_group.id)

        return pocket_group

    def update(self, instance, validated_data):
        """updated pockets must be updated with new values"""
        pockets = validated_data.pop('pockets')
        pocket_ids = (pocket.id for pocket in pockets)
        selected_pockets = Pocket.objects.filter(id__in=pocket_ids)

        saved_pockets = instance.pockets.all()

        new_pockets = selected_pockets.exclude(id__in=saved_pockets)
        removed_pockets = saved_pockets.exclude(id__in=selected_pockets)

        new_pockets.update(pocket_group=instance.id)
        removed_pockets.update(pocket_group=None)

        instance.title = validated_data.get('title', instance.title)

        return instance
