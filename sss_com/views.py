import json

from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from datetime import datetime

@api_view(['GET', 'POST'])
def index(request):
    print()
    print("Request:", request)
    query_params = request.query_params.dict()
    body_data = json.loads(request.body)
    print("Params:", query_params)
    print("Body:", body_data)
    print()
    data = {
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "status": "GOOD",
        "origin-message-params": str(query_params),
        "origin-message-body": str(body_data)
    }
    return JsonResponse(data, status=200)


@api_view(['GET', 'POST'])
def user(request):
    print()
    print("Request:", request)
    query_params = request.query_params.dict()
    body_data = json.loads(request.body)
    print("Params:", query_params)
    print("Body:", body_data)
    print()
    data = {
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "status": "GOOD",
        "origin-message-params": str(query_params),
        "origin-message-body": str(body_data)
    }
    return JsonResponse(data, status=200)

@api_view(['GET', 'POST'])
def provider(request):
    print()
    print("Request:", request)
    query_params = request.query_params.dict()
    body_data = json.loads(request.body)
    print("Params:", query_params)
    print("Body:", body_data)
    print()
    data = {
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "status": "GOOD",
        "origin-message-params": str(query_params),
        "origin-message-body": str(body_data)
    }
    return JsonResponse(data, status=200)
