from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Devices, Temperatures, Pressures, Altitudes

def home(request):
    return HttpResponse("Bienvenue sur l'application IoT !")

def viewdevice(request, device_id):
    device = get_object_or_404(Devices, pk=device_id)
    temperatures = Temperatures.objects.filter(device=device).order_by("-createdAt")[:1000]
    pressures = Pressures.objects.filter(device=device).order_by("-createdAt")[:1000]
    altitude = Altitudes.objects.filter(device=device).order_by("-createdAt")[:1000]
    context = {
        "device": device,
        "temperatures": temperatures,
        "pressures": pressures,
        "altitude": altitude
    }
    return render(request, "html/viewdevice.html", context)

def device_list(request):
    devices = Devices.objects.order_by("-lastSeenAt")
    pressures = Pressures.objects.all()
    altitudes = Altitudes.objects.all()
    temperatures = Temperatures.objects.all()
    last_altitude = altitudes.last().value if altitudes.exists() else 0
    last_pressure = pressures.last().value if pressures.exists() else 0
    context = {
        'devices': devices,
        'temperatures': temperatures,
        'pressures': pressures,
        'altitudes': altitudes,
        'last_altitude': last_altitude,
        'last_pressure': last_pressure,
    }
    return render(request, "html/deviceslist.html", context)
