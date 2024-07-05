from doctest import Example
import os
import psycopg2
import openai
from crewai import Agent, Task, Crew, Process
from crewai_tools import FileReadTool

os.environ["OPENAI_API_KEY"] = ''
# os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o'
# os.environ["OPENAI_MODEL_NAME"] = 'asst_ZFpHdek1zkd71kqUoFQX4vfW'

openai.api_key = os.getenv("OPENAI_API_KEY")
schema_tool = FileReadTool(file_path='schema.txt')
instructions_tool = FileReadTool(file_path='instructions.txt')

sql_generator = Agent(
    role='Postgress SQL Query Generator',
    goal='Generate Postgress SQL query based on this requirements {input}',
    tools=[schema_tool],
    verbose=True,
    backstory=(
        "You are an expert in Postgress SQL and can understand complex database structures and user requirements to generate precise Postgress SQL queries. create a query that will meet this requirements {input}"
    )
)

generate_sql_task = Task(
    description=(
        "Take user input and generate an Postgress SQL query based on the provided information. "
        "The input could be a natural language description of what data needs to be fetched. "
        "Ensure that the Postgress SQL query is optimized and accurate. "
        "Add double quotation mark on all tables names and all fields names"
        "Use the Prisma schema to understand the database structure."
        "Create a query based on {input}"
    ),
    tools=[schema_tool],
    verbose=True,
    expected_output='A valid SQL query string that matches requirements for {input}.',
    agent=sql_generator
)

add_quotes_task = Task(
    description=(
        "Take an Postgress SQL query an add quotes on every field or table name"
    ),
    verbose=True,
    expected_output='A valid SQL query string that matches requirements for {input}.',
    agent=sql_generator
)

crew = Crew(
    agents=[sql_generator],
    memory=False,
    tasks=[generate_sql_task, add_quotes_task],
    process=Process.sequential,
)

def kickoff_sql_generation(user_input):
    result = crew.kickoff(inputs={"input": user_input})
    
    if isinstance(result, str):
        result =  result.replace("```sql", "").replace("```", "").strip()

    return result

# user_input = "count of all users older than 18"
user_input = "get all users activated last month that is a manager"

result = kickoff_sql_generation(user_input)
print(result)

def sql_execute(result):
    sql_query = result

    db_params = {
        'dbname': 'postgres',
        'user': 'admin',
        'password': '12345678',
        'host': 'localhost',
        'port': '54322'
    }

    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        cursor.execute(sql_query)
        query_results = cursor.fetchall()

        print('*******')
        print('*******')
        print('*******')
        print('*******')
        print(query_results)

        cursor.close()
        conn.close()

        return query_results
    
    except Exception as e:
            print(f"Error executing SQL query: {e}")

sql_execute(result)

