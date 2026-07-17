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


# Quick manual test (only runs if you run this file directly)
if __name__ == "__main__":
    output = query_semantic_layer("revenue", "transaction__region")
    print(output)