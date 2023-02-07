from django.db import models
from core.models import CommonAddress, CommonLocation

class Talep(models.Model):
    location = models.ForeignKey("taleps.TalepLocation", on_delete=models.CASCADE)
    source = models.CharField(max_length=255, null=True)
    extra_info = models.JSONField()

    class Meta:
        ordering = ["-id"]


class TalepLocation(CommonLocation):
    address = models.ForeignKey("taleps.TalepAddress", on_delete=models.CASCADE)


class TalepAddress(CommonAddress):
    pass