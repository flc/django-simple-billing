from django.utils.translation import ugettext_lazy as _

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

        required = ('address_1', 'city', 'country', 'post_code')
        for name, field in self.fields.items():
            if name in required:
                field.required = True

    def validate(self, attrs):
        company = attrs['company_name']
        first_name = attrs['first_name']
        last_name = attrs['last_name']
        if not company:
            if not first_name or not last_name:
                error = _(
                "You have to specify either the first name "
                "and last name or the company name."
                )
                raise serializers.ValidationError(error)
        return attrs

    def save_object(self, obj, **kwargs):
        ret = super(BillingDataSerializer, self).save_object(obj, **kwargs)
        if self.user:
            ub = UserBilling.objects.get_or_create(
                user=self.user,
                defaults={'billing': obj},
                )
        return ret
