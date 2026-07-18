from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

from tools import query_semantic_layer, query_breakdown

llm = ChatOllama(model="llama3.2", temperature=0)


def investigate_margin_drop() -> str:
    """
    Deterministic investigation: find the worst quarter, then find the
    product/region driving it. Python controls the steps reliably;
    the AI only explains the findings at the end.
    """
    # Step 1: get margin by quarter
    margin_by_quarter = query_semantic_layer("margin", "metric_time__quarter")

    # Step 2: parse out the quarter with the lowest margin
    # (simple text parsing of the markdown table MetricFlow returns)
    lines = [l for l in margin_by_quarter.splitlines() if l.startswith("|") and "-01" in l]
    worst_quarter = None
    worst_margin = 999
    for line in lines:
        parts = [p.strip() for p in line.split("|") if p.strip()]
        if len(parts) == 2:
            date_str, margin_str = parts
            try:
                margin_val = float(margin_str)
                if margin_val < worst_margin:
                    worst_margin = margin_val
                    worst_quarter = date_str
            except ValueError:
                continue

    if not worst_quarter:
        return "Could not determine the worst quarter from the data."

    # Step 3: calculate quarter end date (roughly, 3 months later)
    from datetime import datetime
    start = datetime.strptime(worst_quarter, "%Y-%m-%d")
    end_month = start.month + 2
    end_year = start.year
    if end_month > 12:
        end_month -= 12
        end_year += 1
    end = datetime(end_year, end_month, 28)

    # Step 4: get cost breakdown by product for that specific quarter
    breakdown = query_breakdown(
        "cost", "transaction__product",
        start_time=start.strftime("%Y-%m-%d"),
        end_time=end.strftime("%Y-%m-%d")
    )

    # Step 5: ask the AI to just explain the findings (no tool calling needed!)
    prompt = f"""
You are a business analyst. Here is data about a margin drop investigation:

Margin by quarter:
{margin_by_quarter}

The worst quarter was {worst_quarter} with a margin of {worst_margin}.

Cost breakdown by product for that specific quarter:
{breakdown}

Explain in 2-3 clear sentences what happened and which product/quarter caused the margin drop, citing the specific numbers.
"""
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content


if __name__ == "__main__":
    result = investigate_margin_drop()
    print("\n\nFINAL ANSWER:", result)