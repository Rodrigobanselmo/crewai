import os

import psycopg2
from crewai import Agent, Crew, Process, Task
from crewai_tools import FileReadTool, tool
from openai import OpenAI

os.environ["OPENAI_API_KEY"] = ''
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o'

client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")

response = client.completions.create(
    model="asst_ZFpHdek1zkd71kqUoFQX4vfW",
    prompt="whats is the size of earth",
    max_tokens=150
)

print(response)
