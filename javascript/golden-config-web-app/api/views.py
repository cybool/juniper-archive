from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Devices
from .serializers import DeviceSerializer


@csrf_exempt
def device_list(request):
    ### #######################################################
    ### RETURN A LIST OF DEVICES
    ### #######################################################
    if request.method == 'GET':
        devices = Devices.objects.all()
        serializer = DeviceSerializer(devices, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = DeviceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        Devices.objects.all().delete()
        return HttpResponse(status=204)


@csrf_exempt
def device_detail(request, pk):
    ### #######################################################
    ### RETURN DETAILS OF A DEVICE
    ### #######################################################
    try:
        device = Devices.objects.get(pk=pk)
    except:
        return HttpResponse(status=404)
    
    if request.method == 'GET':
        serializer = DeviceSerializer(device)
        return JsonResponse(serializer.data)
    
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = DeviceSerializer(device, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    
    elif request.method == 'DELETE':
        device.delete()
        return HttpResponse(status=204)
