from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from django_countries import countries

from .serializers import BillingDataSerializer
from .models import UserBilling


class BillingView(generics.GenericAPIView):
    serializer_class = BillingDataSerializer
    permission_classes = (
        IsAuthenticated,
        )

    def _get_object(self, request):
        ub = UserBilling.objects.get(user=request.user)
        return ub.billing

    def get(self, request):
        billing = self._get_object(request)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(billing)
        return Response(serializer.data)

    def post(self, request):
        billing = self._get_object(request)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.DATA, instance=billing)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CountriesView(APIView):
    permission_classes = (
        IsAuthenticated,
        )

    def get(self, request):
        return Response({'countries': countries})
