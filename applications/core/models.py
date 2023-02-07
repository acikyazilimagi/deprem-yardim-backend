from django.db import models

class CommonLocation(models.Model):
    formatted_address = models.TextField(null=True, blank=True)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    northeast_lat = models.FloatField(default=0.0)
    northeast_lng = models.FloatField(default=0.0)
    southwest_lat = models.FloatField(default=0.0)
    southwest_lng = models.FloatField(default=0.0)
    is_approved = models.BooleanField(default=False)

    @property
    def loc(self):
        return [self.latitude, self.longitude]

    @property
    def viewport(self):
        return {
            "northeast": {"lat": self.northeast_lat, "lng": self.northeast_lng},
            "southwest": {"lat": self.southwest_lat, "lng": self.southwest_lng},
        }

    class Meta:
        ordering = ["-id"]
        abstract = True


class CommonAddress(models.Model):
    address = models.TextField()
    city = models.CharField(max_length=255, null=True, blank=True)
    distinct = models.CharField(max_length=255, null=True, blank=True)
    neighbourhood = models.CharField(max_length=255, null=True, blank=True)
    street = models.CharField(max_length=255, null=True, blank=True)
    no = models.CharField(max_length=255, null=True, blank=True)
    name_surname = models.CharField(max_length=255, null=True, blank=True)
    tel = models.CharField(max_length=255, null=True, blank=True)
    is_resolved = models.BooleanField(default=False)

    class Meta:
        ordering = ["-id"]
        abstract = True