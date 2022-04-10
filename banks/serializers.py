from rest_framework import serializers

from .models import Bank, Account, Vault


class VaultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vault
        fields = '__all__'
        read_only_fields = ('user',)


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
        read_only_fields = ('user',)

    vaults = VaultSerializer(many=True, read_only=True)


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'
        read_only_fields = ('user',)

    accounts = AccountSerializer(many=True, read_only=True)
