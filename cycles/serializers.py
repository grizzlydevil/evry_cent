from email.policy import default
from rest_framework import serializers

from .models import Cycle, Income, IncomeDistributor
from banks.models import Account
from goals.models import Pocket


class FieldValuesFilteredByUser(serializers.PrimaryKeyRelatedField):
    """
    This class filters foreign key to current user and active field values only
    """
    def get_queryset(self):
        user = self.context['request'].user
        if self.field_name == 'account':
            field_values = Account.objects.filter(bank__user=user)
        elif self.field_name == 'cycle':
            field_values = Cycle.objects.filter(user=user)
        elif self.field_name == 'pocket':
            field_values = Pocket.objects.filter(wallet__goal__user=user)

        return field_values


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = '__all__'

    cycle = FieldValuesFilteredByUser()
    account = FieldValuesFilteredByUser()

    def validate_cycle(self, value):
        if value.user != self.context['request'].user:
            raise serializers.ValidationError('invalid cycle')

        return value

    def validate_account(self, value):
        if value.bank.user != self.context['request'].user:
            raise serializers.ValidationError('invalid account')

        return value


class IncomeDistributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeDistributor
        fields = '__all__'

    cycle = FieldValuesFilteredByUser()
    pocket = FieldValuesFilteredByUser()

    money_in = serializers.DecimalField(max_digits=12, decimal_places=2,
                                        min_value=0.00, default=0.00,
                                        initial=0.00)
    in_outside_salary = serializers.DecimalField(max_digits=12,
                                                 decimal_places=2,
                                                 min_value=0.00, default=0.00,
                                                 initial=0.00)
    out = serializers.DecimalField(max_digits=12, decimal_places=2,
                                   min_value=0.00, default=0.00, initial=0.00)

    def validate_cycle(self, value):
        """Validate cycle is of this user."""
        if value.user != self.context['request'].user:
            raise serializers.ValidationError('invalid cycle')

        return value

    def validate_pocket(self, value):
        """validate pocket is of this user"""
        if value.wallet.goal.user != self.context['request'].user:
            raise serializers.ValidationError('invalid pocket')

        return value

    def validate(self, data):
        """validate only a single distributor can exist for 1 pocket/1 cycle"""
        selected_cycle = data['cycle']
        selected_pocket = data['pocket']

        if (
            IncomeDistributor.objects.
            filter(cycle=selected_cycle).
            filter(pocket=selected_pocket).
            exists()
        ):
            raise serializers.ValidationError(
                'too many distributors per 1 cycle in 1 pocket')
        return data


class CycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cycle
        fields = '__all__'
        read_only_fields = ('user',)

    incomes = IncomeSerializer(many=True, read_only=True)
    distributors = IncomeDistributorSerializer(many=True, read_only=True)

    def validate(self, data):
        """check if start is before end"""
        end_date = data.get('end_date')
        if end_date and data['start_date'] > end_date:
            raise serializers.ValidationError(
                'Start date must be before end date')

        return data

    def create(self, validated_data):
        """Create income distributors for every active pocket"""
        cycle_instance = super().create(validated_data)

        active_pockets = (
            Pocket.objects
            .filter(wallet__goal__user=self.context['request'].user)
            .filter(active=True)
        )

        distributors = []
        for pocket in active_pockets:
            distributors.append(IncomeDistributor(cycle=cycle_instance,
                                                  pocket=pocket))

        IncomeDistributor.objects.bulk_create(distributors)

        return cycle_instance
