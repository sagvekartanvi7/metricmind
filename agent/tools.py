import subprocess
import os

MF_PATH = r"D:\AXLERO\metricmind\warehouse\venv\Scripts\mf.exe"
DBT_PROJECT_PATH = r"D:\AXLERO\metricmind\warehouse\metricmind_dbt"

def query_semantic_layer(metric: str, group_by: str = "metric_time__quarter") -> str:
    """
    Queries the governed semantic layer (via MetricFlow) for a given metric,
    grouped by a given dimension. Returns the result as text.
    
    Example: query_semantic_layer("revenue", "transaction__region")
    """
    command = [
        MF_PATH, "query",
        "--metrics", metric,
        "--group-by", group_by
    ]

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    result = subprocess.run(
        command,
        cwd=DBT_PROJECT_PATH,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        shell=True,
        env=env
    )

    if result.returncode != 0:
        return f"Error running query: {result.stderr}"

    return result.stdout


def query_breakdown(metric: str, dimension: str, region: str = None,
                     start_time: str = None, end_time: str = None) -> str:
    """
    Queries a metric broken down by a specific dimension, optionally filtered
    by region and/or a time range. Use this to investigate WHY a top-level
    metric changed in a specific period or region.

    Example: query_breakdown("cost", "transaction__product", region="Europe",
                              start_time="2025-04-01", end_time="2025-06-30")
    """
    command = [
        MF_PATH, "query",
        "--metrics", metric,
        "--group-by", dimension
    ]

    if region:
        command += ["--where", f"{{{{ Dimension('transaction__region') }}}} = '{region}'"]

    if start_time:
        command += ["--start-time", start_time]
    if end_time:
        command += ["--end-time", end_time]

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    result = subprocess.run(
        command,
        cwd=DBT_PROJECT_PATH,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        shell=True,
        env=env
    )

    if result.returncode != 0:
        return f"Error running breakdown query: {result.stderr}"

    return result.stdout


# Quick manual test (only runs if you run this file directly)
if __name__ == "__main__":
    output = query_breakdown("cost", "transaction__product", region="Europe",
                              start_time="2025-04-01", end_time="2025-06-30")
    print(output)