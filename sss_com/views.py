from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from datetime import datetime

@api_view(['GET', 'POST'])
def index(request):
    print(request)
    data = {
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "status": "GOOD"
    }
    return JsonResponse(data, status=200)