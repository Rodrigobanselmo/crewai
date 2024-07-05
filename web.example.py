import os
from crewai import Agent, Crew, Task, Process
from crewai_tools import SerperDevTool, ExaSearchTool

os.environ["OPENAI_API_KEY"] = ""
os.environ["SERPER_API_KEY"] = ""
os.environ["EXA_API_KEY"] = ""
os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'

search_tool = SerperDevTool()
exa_search_tool = ExaSearchTool()

researcher = Agent(
  role='Researcher',
  goal='Conduct foundational research',
  backstory='An experienced researcher with a passion for uncovering insights'
)
analyst = Agent(
  role='Data Analyst',
  goal='Analyze research findings',
  backstory='A meticulous analyst with a knack for uncovering patterns'
)
writer = Agent(
  role='Writer',
  goal='Draft the final report',
  backstory='A skilled writer with a talent for crafting compelling narratives'
)

research_task = Task(description='Gather relevant data...', agent=researcher, expected_output='Raw Data')
analysis_task = Task(description='Analyze the data...', agent=analyst, expected_output='Data Insights')
writing_task = Task(description='Compose the report...', agent=writer, expected_output='Final Report')

report_crew = Crew(
  agents=[researcher, analyst, writer],
  tasks=[research_task, analysis_task, writing_task],
  process=Process.sequential
)

result = report_crew.kickoff(inputs={"topic": 'famous diseases'})

print(result)