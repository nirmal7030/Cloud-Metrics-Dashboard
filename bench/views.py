import json
import statistics

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import Metric


# -------------------------------
# UI VIEW – main dashboard page
# -------------------------------
def dashboard(request):
    """
    Render the security metrics dashboard.
    Frontend JavaScript will call /api/metrics/data/ to fetch live data.
    """
    return render(request, "bench/dashboard.html")


# -------------------------------
# API – ingest metrics from CI/CD
# -------------------------------
@csrf_exempt
def api_ingest(request):
    """
    Receive metric data from CI/CD pipeline.

    Expected:
      - HTTP header:  X-Bench-Key: <BENCH_API_KEY>
      - JSON body with fields:
          source, workflow, run_id, run_attempt, branch, commit_sha,
          lce, prt, smo, dept, clbc, value (optional), notes (optional)
    """
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    # Parse JSON
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    # Simple API key check
    api_key = request.headers.get("X-Bench-Key")
    expected_key = getattr(settings, "BENCH_API_KEY", "")
    if api_key != expected_key:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    # Compute overall value if not provided (simple average of 5 metrics)
    if "value" in payload and payload["value"] is not None:
        overall_value = float(payload["value"])
    else:
        parts = [
            payload.get("lce") or 0,
            payload.get("prt") or 0,
            payload.get("smo") or 0,
            payload.get("dept") or 0,
            payload.get("clbc") or 0,
        ]
        overall_value = sum(parts) / 5.0 if any(parts) else 0.0

    # Create a Metric row from the CI payload
    Metric.objects.create(
        # CI/CD context
        source=payload.get("source", "github"),
        workflow=payload.get("workflow", ""),
        run_id=payload.get("run_id", ""),
        run_attempt=payload.get("run_attempt", ""),
        branch=payload.get("branch", ""),
        commit_sha=payload.get("commit_sha", ""),

        # Display name + description used on dashboard
        name=payload.get(
            "name",
            f"{payload.get('source', 'github').title()} – run {payload.get('run_id', '')}"
        ),
        description=payload.get("notes", ""),

        # Overall value + novel metrics
        value=overall_value,
        lce=payload.get("lce") or 0.0,
        prt=payload.get("prt") or 0.0,
        smo=payload.get("smo") or 0.0,
        dept=payload.get("dept") or 0.0,
        clbc=payload.get("clbc") or 0.0,

        # Free-text notes
        notes=payload.get("notes", ""),
    )

    return JsonResponse({"status": "stored"}, status=201)


# -------------------------------
# API – data for dashboard
# -------------------------------
def api_metrics_data(request):
    """
    Return latest metrics (optionally filtered by source)
    in the shape your dashboard expects.

    Query params:
      ?source=github|jenkins|codepipeline (optional)
    """
    source = request.GET.get("source")  # "github", "jenkins", "codepipeline" or None

    qs = Metric.objects.all()
    if source in ["github", "jenkins", "codepipeline"]:
        qs = qs.filter(source=source)

    # Oldest first for a smooth time-series chart
    qs = qs.order_by("created_at")

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
