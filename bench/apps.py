from django.apps import AppConfig


class BenchConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bench"

    def ready(self):
        """
        Seed the database with example metric observations the first time
        the app starts and the table is empty.

        This runs in both local and EC2 environments, but will not
        duplicate data because it checks .exists() first.
        """
        from django.db.utils import OperationalError, ProgrammingError

        try:
            # This is the model we created earlier for your metrics
            from .models import MetricObservation
        except Exception:
            # Model not yet importable
            return

        try:
            # If there are already metrics, do nothing
            if MetricObservation.objects.exists():
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

        except (OperationalError, ProgrammingError):
            # DB tables not ready yet (e.g. during migrate) – just skip
            return
