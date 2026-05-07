from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def compound_interest(request):
    return Response({"message": "Compound interest calculation"})

@api_view(['POST'])
def emergency_fund(request):
    return Response({"message": "Emergency fund calculation"})