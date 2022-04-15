from rest_framework import serializers

from .models import Bank, Account, Vault


class FieldValuesFilteredByUser(serializers.PrimaryKeyRelatedField):
    """
    This class filters foreign key to current user and active field values only
    """
    def get_queryset(self):
        user = self.context['request'].user
        if self.field_name == 'account':
            field_values = Account.objects.filter(bank__user=user)
        elif self.field_name == 'bank':
            field_values = Bank.objects.filter(user=user)

        return field_values


class VaultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vault
        fields = '__all__'

    account = FieldValuesFilteredByUser()

    def validate_account(self, value):
        if value.bank.user != self.context['request'].user:
            raise serializers.ValidationError('invalid account')

        return value


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

    vaults = VaultSerializer(many=True, read_only=True)
    bank = FieldValuesFilteredByUser()

    def validate_bank(self, value):
        if value.user != self.context['request'].user:
            raise serializers.ValidationError('invalid bank')

        return value


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'
        read_only_fields = ('user',)

    accounts = AccountSerializer(many=True, read_only=True)
