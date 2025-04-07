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
    return render(request, "iot/viewdevice.html", context)

def device_list(request):
    devices = Devices.objects.order_by("-lastSeenAt")
    return render(request, "iot/deviceslist.html", {"devices": devices})
