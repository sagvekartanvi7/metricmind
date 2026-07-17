from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain_core.tools import tool

from tools import query_semantic_layer


@tool
def query_semantic_layer_tool(metric: str, group_by: str) -> str:
    """
    Queries the governed semantic layer for a business metric.
    
    Args:
        metric: One of 'revenue', 'cost', or 'margin'.
        group_by: One of 'transaction__region', 'transaction__product',
                  'metric_time__quarter', or 'metric_time__day'.
    """
    return query_semantic_layer(metric, group_by)


# Connect to our local Llama 3.1 model
llm = ChatOllama(model="llama3.1", temperature=0)

agent = create_agent(
    llm,
    tools=[query_semantic_layer_tool],
    system_prompt=(
        "You are MetricMind, a business analytics assistant. "
        "You must ONLY answer using the query_semantic_layer_tool tool — "
        "never make up numbers yourself. "
        "Valid metrics: revenue, cost, margin. "
        "Valid group_by values: transaction__region, transaction__product, "
        "metric_time__quarter, metric_time__day."
    ),
)

if __name__ == "__main__":
    question = "What is our total revenue broken down by region?"
    result = agent.invoke({"messages": [{"role": "user", "content": question}]})

    # Print the final AI message
    final_message = result["messages"][-1]
    print("\n\nFINAL ANSWER:", final_message.content)