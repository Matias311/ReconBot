from django.db import models
from django.utils import timezone


class DomainAnalysis(models.Model):
    domain = models.CharField(max_length=255)
    report = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Domain Analyses"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Análisis de {self.domain} ({self.created_at})"
