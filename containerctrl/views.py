from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import docker
import secrets
import string
import json

from .models import running_container_names

# Create your views here.
@csrf_exempt
def spin_up(request):
    if request.method == 'POST':
        spinup_req = json.loads(request.body.decode('utf-8'))
        service = spinup_req['service']
        qty = spinup_req['qty']
        strategy = spinup_req['strategy']
        client = docker.from_env()
        service_name = ''.join(secrets.choice(string.ascii_lowercase + string.digits)
                      for i in range(10))
        service_name = service + "_" + service_name
        running_container_names.append(service_name)
        print(client.containers.run(service, name = service_name, network_mode = "host", detach=True))
        return JsonResponse({"state":"spinup","service_name":service_name})

@csrf_exempt
def spin_down(request):
    if request.method == 'POST':
        spindown_req = json.loads(request.body.decode('utf-8'))
        service_name = spindown_req['service_name']
        # if service_name in running_container_names:
        if True:
            client = docker.from_env()
            client.containers.get(service_name).stop()
            return JsonResponse({"state": "spindown", "service_name": service_name})
        else:
            return JsonResponse({"state": "error", "error": "not a running service name"})


@csrf_exempt
def spin_restart(request):
    if request.method == 'POST':
        spinrestart_req = json.loads(request.body.decode('utf-8'))
        service_name = spinrestart_req['service_name']
        # if service_name in running_container_names:
        if True:
            client = docker.from_env()
            client.containers.get(service_name).restart()
            return JsonResponse({"state": "restarted", "service_name": service_name})
        else:
            return JsonResponse({"state": "error", "error": "not a running service name"})

@csrf_exempt
def stats(request):
    if request.method == 'POST':
        stats_req = json.loads(request.body.decode('utf-8'))
        service_name = stats_req['service_name']
        # if service_name in running_container_names:
        if True:
            client = docker.from_env()
            container_stats = client.containers.get(service_name).stats(decode=None, stream = False)
            return JsonResponse(container_stats)
        else:
            return JsonResponse({"state": "error", "error": "not a running service name"})
