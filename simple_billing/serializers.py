from rest_framework import serializers

from .utils import get_billing_model


class BillingDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_billing_model()
        exclude = ('id',)

