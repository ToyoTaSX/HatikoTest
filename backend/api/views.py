import json
import os
from pprint import pprint

import requests
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

def get_balance():
    url = "https://api.imeicheck.net/v1/account"

    payload = {}
    headers = {
        'Authorization': f'Bearer {os.getenv("API_TOKEN")}',
        'Accept-Language': 'en',
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return float(response.json()['balance'])

def get_services():
    url = "https://api.imeicheck.net/v1/services"
    payload = {}
    headers = {
        'Authorization': f'Bearer {os.getenv("API_TOKEN")}',
        'Accept-Language': 'en',
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    return data

def get_service(id):
    url = f"https://api.imeicheck.net/v1/services/{id}"

    payload = {}
    headers = {
        'Authorization': 'Bearer ' + os.getenv('API_TOKEN'),
        'Accept-Language': 'en',
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()


class CheckImei(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        imei = request.data.get('imei', None)
        sid = request.data.get('service_id', None)
        if not imei and not sid:
            return Response({"message": 'imei and service_id is required'}, status=400)
        elif not imei:
            return Response({"message": 'imei is required'}, status=400)
        elif not sid:
            return Response({"message": 'service_id is required'}, status=400)

        service = get_service(sid)
        price = service['price']
        if float(price) > get_balance():
            return Response({'message': 'Not enough money'}, status=400)

        url = "https://api.imeicheck.net/v1/checks"

        payload = {
            "deviceId": imei,
            "serviceId": int(sid)
        }
        headers = {
            'Authorization': 'Bearer ' + os.getenv('API_TOKEN'),
            'Accept-Language': 'en',
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        data = response.json()
        if 'errors' in data:
            return Response({'errors': data['errors']}, status=response.status_code)

        return Response({"check": response.json()})

class CheckBalance(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"balance": get_balance()}, status=200)

class GetServices(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"services": get_services()}, status=200)

