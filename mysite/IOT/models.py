from django.db import models

class Devices(models.Model):
    uid = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)  
    createdAt = models.DateTimeField(auto_now_add=True)
    lastSeenAt = models.DateTimeField()

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Device"
        verbose_name_plural = "Devices"

class Temperatures(models.Model):
    device = models.ForeignKey(Devices, on_delete=models.CASCADE)
    value = models.FloatField()
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.device.name} - {self.value}°C"
    class Meta:
        verbose_name = "Temperature"
        verbose_name_plural = "Temperatures"
    
class Pressures(models.Model):
    device = models.ForeignKey(Devices, on_delete=models.CASCADE)
    value = models.FloatField()
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.device.name} - {self.value}Pa"
    class Meta:
        verbose_name = "Pression"
        verbose_name_plural = "Pressions"

class Altitudes(models.Model):
    device = models.ForeignKey(Devices, on_delete=models.CASCADE)
    value = models.FloatField()
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.device.name} - {self.value}m"
    class Meta:
        verbose_name = "Altitude"
        verbose_name_plural = "Altitudes"