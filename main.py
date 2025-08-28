from agents import Agent, AsyncOpenAI, Runner, OpenAIChatCompletionsModel, handoff, function_tool
import os
from dotenv import load_dotenv
from tavily import TavilyClient
import json
from agents.extensions import handoff_filters

load_dotenv()

premium_user = True

if premium_user:
    basic_writer= False
else:
    basic_writer = True

external_client = AsyncOpenAI(
    base_url="https://api.deepseek.com/v1",
    api_key=os.getenv("DEEPSEEK_API_KEY")
)

llm = OpenAIChatCompletionsModel(
    model="deepseek-reasoner",
    openai_client=external_client
)

gemini_llm = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=AsyncOpenAI(
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        api_key=os.getenv("Gemini_API_KEY"),
    )
)
gemini_pro_llm = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=AsyncOpenAI(
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        api_key=os.getenv("Gemini_API_KEY"),
    )
)



@function_tool
def get_more_info(query: str) -> str:
    """
    get more information from the user if needed.
    query: explanation from llm i.e. what particular information it needs
    resp : user provided information
    """
    print(query)
    resp = input("please provide more information: ")
    return resp

@function_tool
def web_search(query: str) -> str:
    """
    Perform a web search using the Tavily API.
    """
    client = TavilyClient()
    response = client.search(query)
    return response

professional_writer = Agent(
    name="professional writer",
    instructions="""
    you are responsible for writing high-quality content. make sure to follow the guidelines provided.
    make a comprehensive report based on information provided.
    """,
    model=gemini_llm,
)

premium_professional_writer = Agent(
     name="professional writer",
    instructions="""
    you are responsible for writing high-quality content. make sure to follow the guidelines provided.
    make sure to add source checking, conflict detection, synthesis and citation system. write it like NYT or bloomberg article 
    make a comprehensive report based on information provided.
    """,
    model=gemini_pro_llm,
)

web_search_agent= Agent(
    name="web search agent",
    instructions="""
    you are responsible for web search only make sure to find the most relevant information.
    add sources. then delegate the information gathered to assist the professional writer.
    """,
    model=gemini_llm,
    tools=[web_search],
    handoffs=[handoff(agent=professional_writer,input_filter=handoff_filters.remove_all_tools ,is_enabled=basic_writer), handoff(agent=premium_professional_writer, is_enabled=premium_user)]
)

planning_agent = Agent(
    name="planner",
    instructions="""
    you are responsible for planning the task at hand. make sure to break down the task into smaller sub-tasks if needed.
    make a sound plan for execution. Make sure to inform what information should be added and what not. 
    delegate task to next agent if neccessary
    """,
    model=llm,
    handoffs=[handoff(agent=web_search_agent)],
)


agent = Agent(
    name="helping agent",
    instructions="""
    You are a helpful agent that can perform complex tasks by planning, and asking the user for more information when needed.
    You can delegate to: planning agent
    """,
    model=gemini_llm,
    tools=[get_more_info],
    handoffs=[handoff(agent=planning_agent, input_filter=handoff_filters.remove_all_tools)],
)

user_query = input("What is your query?: ")
response = Runner.run_sync(agent,user_query)
print(response.final_output)
