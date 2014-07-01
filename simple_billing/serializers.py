from rest_framework import serializers

from .utils import get_billing_model
from .models import UserBilling


class BillingDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_billing_model()
        exclude = ('id',)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(BillingDataSerializer, self).__init__(*args, **kwargs)

    def save_object(self, obj, **kwargs):
        ret = super(BillingDataSerializer, self).save_object(obj, **kwargs)
        if self.user:
            ub = UserBilling.objects.get_or_create(
                user=self.user,
                defaults={'billing': obj},
                )
        return ret
