import json
import pandas as pd

from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from datetime import datetime
from ipware import get_client_ip
from sss_com.run_NN_model import runNNmodel
from sss_com.variables import user_is_waiting

        #testbssidlist = ["bc:f3:10:33:d5:74","06:23:aa:02:31:02","00:23:aa:64:3e:e5","00:23:aa:02:31:00","06:23:aa:02:31:03",
        #         "00:23:aa:02:30:b0","0a:23:aa:02:30:b2","0a:23:aa:02:30:b3","42:2f:86:fa:e1:ac","12:23:aa:b5:6c:3a"]
        #testrssilist = [-64, -64, -64, -65, -65, -65, -66, -66, -66, -66]
        #print(runNNmodel(testbssidlist, testrssilist))

@api_view(['GET', 'POST'])
def index(request):
    print("IP:", get_client_ip(request))
    query_params = request.query_params.dict()
    body_data = json.loads(request.body)
    print("Params:", query_params)
    print("Body:", body_data)
    print()
    data = {}
    return JsonResponse(data, status=200)


@api_view(['GET', 'POST'])
def user(request):
    print("IP:", get_client_ip(request))
    query_params = request.query_params.dict()
    body_data = json.loads(request.body)
    print("Params:", query_params)
    print("Body:", body_data)
    print()
    if True:
        bssid_list = []
        bssid_list.append(body_data["BSSID0"])
        bssid_list.append(body_data["BSSID1"])
        bssid_list.append(body_data["BSSID2"])
        bssid_list.append(body_data["BSSID3"])
        bssid_list.append(body_data["BSSID4"])
        bssid_list.append(body_data["BSSID5"])
        bssid_list.append(body_data["BSSID6"])
        bssid_list.append(body_data["BSSID7"])
        bssid_list.append(body_data["BSSID8"])
        bssid_list.append(body_data["BSSID9"])
    
        rssi_list = []
        rssi_list.append(body_data["RSSI0"])
        rssi_list.append(body_data["RSSI1"])
        rssi_list.append(body_data["RSSI2"])
        rssi_list.append(body_data["RSSI3"])
        rssi_list.append(body_data["RSSI4"])
        rssi_list.append(body_data["RSSI5"])
        rssi_list.append(body_data["RSSI6"])
        rssi_list.append(body_data["RSSI7"])
        rssi_list.append(body_data["RSSI8"])
        rssi_list.append(body_data["RSSI9"])

        global user_is_waiting
        user_is_waiting = runNNmodel(bssid_list, rssi_list)
        data = {
            "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "status": "GOOD",
            "origin-message-params": str(query_params),
            "origin-message-body": str(body_data),
            "location": user_is_waiting
        }
    return JsonResponse(data, status=200)

@api_view(['GET', 'POST'])
def provider(request):
    print("IP:", get_client_ip(request))
    query_params = request.query_params.dict()
    body_data = json.loads(request.body)
    print("Params:", query_params)
    print("Body:", body_data)
    print()
    if body_data["method"] == "look":
        global user_is_waiting
        if user_is_waiting:
            data = {
                "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "status": "GOOD",
                "alarm": "None"   
            }
        else:
            data = {
                "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "status": "GOOD",
                "alarm": user_is_waiting   
            }
            user_is_waiting = 0 

    elif body_data["method"] == "scan":
        data = {
            "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "status": "GOOD",
            "origin-message-params": str(query_params),
            "origin-message-body": str(body_data)
        }
    else:
        data = {
            "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "status": "BAD",
            "error": "unknown method"         
        }
    return JsonResponse(data, status=200)
