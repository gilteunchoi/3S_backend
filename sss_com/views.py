import json

from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from datetime import datetime
from ipware import get_client_ip
from sss_com.run_NN_model import runNNmodel

@api_view(['GET', 'POST'])
def index(request):
    print("IP:", get_client_ip(request))
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
    print("IP:", get_client_ip(request))
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
    if True:
        testbssidlist = ["bc:f3:10:33:d5:74","06:23:aa:02:31:02","00:23:aa:64:3e:e5","00:23:aa:02:31:00","06:23:aa:02:31:03",
                 "00:23:aa:02:30:b0","0a:23:aa:02:30:b2","0a:23:aa:02:30:b3","42:2f:86:fa:e1:ac","12:23:aa:b5:6c:3a"]
        testrssilist = [-64, -64, -64, -65,	-65, -65, -66, -66,	-66, -66]
        print(runNNmodel(testbssidlist, testrssilist))
    return JsonResponse(data, status=200)

@api_view(['GET', 'POST'])
def provider(request):
    print("IP:", get_client_ip(request))
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
