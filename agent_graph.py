from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import Tool
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
import math

# 1. Define a safe Calculator Tool
def calculator_func(expression: str) -> str:
    try:
        return str(eval(expression, {"__builtins__": {}}, {"math": math}))
    except Exception as e:
        return f"Error: {e}"

calculator_tool = Tool(
    name="Calculator",
    func=calculator_func,
    description="Useful for evaluating mathematical expressions. Input should be a valid python math expression string (e.g., '234 * 87 / 3')."
)

# 2. Define the Web Search Tool
search_tool = DuckDuckGoSearchRun(
    name="web_search", 
    description="Search the internet for current information, news, or facts."
)

tools = [search_tool, calculator_tool]

# 3. Initialize the Local LLM 
# Note: llama3.2 works, but if it struggles with tool formatting, run 'ollama pull qwen2.5' and change this to "qwen2.5"
llm = ChatOllama(model="llama3.2", temperature=0)

# 4. Create the LangGraph ReAct Agent
agent_executor = create_react_agent(llm, tools, debug=False)

def run_agent(query: str):
    inputs = {"messages": [HumanMessage(content=query)]}
    for step in agent_executor.stream(inputs, stream_mode="values"):
        messages = step["messages"]
        yield messages[-1]
