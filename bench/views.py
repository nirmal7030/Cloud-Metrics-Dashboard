import json
import statistics

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import Metric


# =======================
#  UI: Dashboard page
# =======================

def dashboard_view(request):
    """
    Render the main dashboard UI.
    """
    return render(request, "bench/dashboard.html")


# Backwards compatibility for bench.ui_urls that uses `views.dashboard`
dashboard = dashboard_view


# =======================
#  API: Ingest metrics
# =======================

@csrf_exempt
def api_ingest(request):
    """
    Receive metric data from the CI/CD pipeline and store a Metric row.

    This version only uses fields that exist on your current Metric model:
        name, description, value, lce, prt, smo, dept, clbc
    """
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    # --- parse JSON body safely ---
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    # --- simple API key check ---
    api_key = request.headers.get("X-Bench-Key")
    expected = getattr(settings, "BENCH_API_KEY", "")
    if not expected or api_key != expected:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    # --- extract metric values (default 0.0) ---
    lce = float(payload.get("lce") or 0.0)
    prt = float(payload.get("prt") or 0.0)
    smo = float(payload.get("smo") or 0.0)
    dept = float(payload.get("dept") or 0.0)
    clbc = float(payload.get("clbc") or 0.0)

    numbers = [lce, prt, smo, dept, clbc]
    value = sum(numbers) / len(numbers) if any(numbers) else 0.0

    # Human-readable name / description
    workflow = payload.get("workflow") or ""
    run_id = payload.get("run_id") or ""
    source = payload.get("source") or "github"

    # Example name: "github – run 123456"
    name = payload.get("name") or f"{source} – run {run_id}".strip(" –")
    description = payload.get("notes", "")

    # --- create Metric row (only fields your model actually has) ---
    Metric.objects.create(
        name=name,
        description=description,
        value=value,
        lce=lce,
        prt=prt,
        smo=smo,
        dept=dept,
        clbc=clbc,
    )

    return JsonResponse({"status": "stored"}, status=201)


# =======================
#  API: Metrics data for dashboard
# =======================

def api_metrics_data(request):
    """
    Return latest metrics for the dashboard.
    """
    qs = Metric.objects.all().order_by("created_at")  # oldest first

    rows = [
        {
            "t": m.created_at.isoformat(),
            "name": m.name,
            "value": m.value,
            "lce": m.lce,
            "prt": m.prt,
            "smo": m.smo,
            "dept": m.dept,
            "clbc": m.clbc,
        }
        for m in qs
    ]

    def avg(key):
        vals = [r[key] for r in rows if r[key] is not None]
        return round(statistics.fmean(vals), 2) if vals else 0.0

    data = {
        "rows": rows,
        "count": len(rows),
        "avg_value": avg("value"),
        "avg_lce": avg("lce"),
        "avg_prt": avg("prt"),
        "avg_smo": avg("smo"),
        "avg_dept": avg("dept"),
        "avg_clbc": avg("clbc"),
    }
    return JsonResponse(data)
