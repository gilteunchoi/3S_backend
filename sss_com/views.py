from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from datetime import datetime

@api_view(['GET', 'POST'])
def index(request):
    print(request)
    query_params = request.query_params.dict()
    print(query_params)
    data = {
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "status": "GOOD",
        "origin-message": str(query_params)
    }
    return JsonResponse(data, status=200)