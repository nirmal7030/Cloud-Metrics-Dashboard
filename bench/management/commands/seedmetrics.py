from django.core.management.base import BaseCommand
from bench.models import MetricObservation


class Command(BaseCommand):
    help = "Seeds the database with example security metrics if empty."

    def handle(self, *args, **options):
        if MetricObservation.objects.exists():
            self.stdout.write(self.style.WARNING("Metrics already exist. Skipping seeding."))
            return

        sample_data = [
            MetricObservation(
                name="GitHub Actions – Baseline",
                value=78,
                lce=0.82,
                prt=0.65,
                smo=0.71,
                dept=0.55,
                clbc=0.48,
            ),
            MetricObservation(
                name="GitHub Actions – Hardened",
                value=84,
                lce=0.88,
                prt=0.71,
                smo=0.77,
                dept=0.61,
                clbc=0.52,
            ),
            MetricObservation(
                name="Jenkins – Baseline",
                value=74,
                lce=0.79,
                prt=0.62,
                smo=0.69,
                dept=0.53,
                clbc=0.46,
            ),
            MetricObservation(
                name="Jenkins – Hardened",
                value=81,
                lce=0.86,
                prt=0.69,
                smo=0.75,
                dept=0.59,
                clbc=0.50,
            ),
            MetricObservation(
                name="AWS CodePipeline – Baseline",
                value=76,
                lce=0.80,
                prt=0.64,
                smo=0.70,
                dept=0.56,
                clbc=0.47,
            ),
            MetricObservation(
                name="AWS CodePipeline – Hardened",
                value=88,
                lce=0.91,
                prt=0.76,
                smo=0.82,
                dept=0.66,
                clbc=0.55,
            ),
        ]

        MetricObservation.objects.bulk_create(sample_data)
        self.stdout.write(self.style.SUCCESS("Seeded sample CI/CD security metrics."))
