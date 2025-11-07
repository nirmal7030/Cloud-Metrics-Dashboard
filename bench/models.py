from django.db import models


class Metric(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    # Main value (overall score or metric)
    value = models.FloatField(default=0.0)

    # Your novel short metrics
    lce = models.FloatField(default=0.0)
    prt = models.FloatField(default=0.0)
    smo = models.FloatField(default=0.0)
    dept = models.FloatField(default=0.0)
    clbc = models.FloatField(default=0.0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
