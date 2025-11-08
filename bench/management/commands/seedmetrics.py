from django.core.management.base import BaseCommand
from bench.models import Metric


class Command(BaseCommand):
    help = "Seeds the database with example CI/CD security metrics if empty."

    def handle(self, *args, **options):
        # Prevent duplicate seeding
        if Metric.objects.exists():
            self.stdout.write(self.style.WARNING("Metrics already exist. Skipping seeding."))
            return

        # Predefined metric entries
        sample_data = [
            Metric(
                name="GitHub Actions – Baseline",
                description="Default GitHub Actions pipeline configuration",
                value=78,
                lce=0.82,
                prt=0.65,
                smo=0.71,
                dept=0.55,
                clbc=0.48,
            ),
            Metric(
                name="GitHub Actions – Hardened",
                description="Enhanced GitHub Actions with security best practices",
                value=84,
                lce=0.88,
                prt=0.71,
                smo=0.77,
                dept=0.61,
                clbc=0.52,
            ),
            Metric(
                name="Jenkins – Baseline",
                description="Standard Jenkins pipeline without hardening",
                value=74,
                lce=0.79,
                prt=0.62,
                smo=0.69,
                dept=0.53,
                clbc=0.46,
            ),
            Metric(
                name="Jenkins – Hardened",
                description="Jenkins pipeline with advanced security controls",
                value=81,
                lce=0.86,
                prt=0.69,
                smo=0.75,
                dept=0.59,
                clbc=0.50,
            ),
            Metric(
                name="AWS CodePipeline – Baseline",
                description="Default AWS CodePipeline configuration",
                value=76,
                lce=0.80,
                prt=0.64,
                smo=0.70,
                dept=0.56,
                clbc=0.47,
            ),
            Metric(
                name="AWS CodePipeline – Hardened",
                description="CodePipeline integrated with security and compliance checks",
                value=88,
                lce=0.91,
                prt=0.76,
                smo=0.82,
                dept=0.66,
                clbc=0.55,
            ),
        ]

        # Insert into DB
        Metric.objects.bulk_create(sample_data)
        self.stdout.write(self.style.SUCCESS("Seeded sample CI/CD security metrics successfully."))
