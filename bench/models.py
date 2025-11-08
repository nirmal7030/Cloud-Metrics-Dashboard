from django.db import models


class Metric(models.Model):
    # -----------------------------
    # CI/CD sources
    # -----------------------------
    SOURCE_GITHUB = "github"
    SOURCE_JENKINS = "jenkins"
    SOURCE_CODEPIPELINE = "codepipeline"

    SOURCE_CHOICES = [
        (SOURCE_GITHUB, "GitHub Actions"),
        (SOURCE_JENKINS, "Jenkins"),
        (SOURCE_CODEPIPELINE, "AWS CodePipeline"),
    ]

    # -----------------------------
    # Metadata
    # -----------------------------
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # -----------------------------
    # CI/CD contextual information
    # -----------------------------
    source = models.CharField(
        max_length=32,
        choices=SOURCE_CHOICES,
        default=SOURCE_GITHUB,
    )
    workflow = models.CharField(max_length=128, blank=True, default="")
    run_id = models.CharField(max_length=64, blank=True, default="")
    run_attempt = models.CharField(max_length=16, blank=True, default="")
    branch = models.CharField(max_length=128, blank=True, default="")
    commit_sha = models.CharField(max_length=64, blank=True, default="")

    # -----------------------------
    # Descriptive information for dashboard
    # -----------------------------
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    # -----------------------------
    # Overall score (can be derived or manual)
    # -----------------------------
    value = models.FloatField(default=0.0)

    # -----------------------------
    # Novel metrics (live values)
    # -----------------------------
    lce = models.FloatField(default=0.0)   # Layer Cache Efficiency
    prt = models.FloatField(default=0.0)   # Pipeline Recovery Time
    smo = models.FloatField(default=0.0)   # Secrets Management Overhead
    dept = models.FloatField(default=0.0)  # Dynamic Env Provisioning Time
    clbc = models.FloatField(default=0.0)  # Cross-Layer Build Consistency

    # -----------------------------
    # Notes or status message
    # -----------------------------
    notes = models.CharField(max_length=255, blank=True, default="")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.source} - {self.name}"
