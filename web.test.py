import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, EXASearchTool

os.environ["OPENAI_API_KEY"] = ""
os.environ["SERPER_API_KEY"] = ""
os.environ["EXA_API_KEY"] = ""
os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'

search_tool = SerperDevTool()
exa_search_tool = EXASearchTool()

researcher = Agent(
    role='Pesquisador',
    goal='Identificar doenças recentes em cidades específicas no Brasil',
    backstory="Você é habilidoso em encontrar e documentar os mais recentes surtos de doenças. Sua expertise ajuda na identificação precoce e mitigação.",
    memory=True,
    verbose=True,
    allow_delegation=False,
    tools=[search_tool],
    allow_code_execution=False,
    max_iter=15,
    max_rpm=100,
    max_execution_time=3600,
)

analyst = Agent(
    role='Analista',
    goal='Analisar os dados sobre doenças recentes e fornecer insights',
    backstory="Com um olhar atento para detalhes, você analisa dados complexos para descobrir tendências e insights que são cruciais para o controle e prevenção de doenças.",
    verbose=True,
    allow_delegation=False,
    memory=True,
    tools=[exa_search_tool],
)

manager = Agent(
  role='Gerente',
  goal='Garantir o bom funcionamento e coordenação da equipe',
  verbose=True,
  backstory="Como um experiente gerente de projetos, você é excelente em organizar tarefas, gerenciar prazos e garantir que a equipe permaneça no caminho certo.",
  allow_code_execution=True,
)

search_task = Task(
    description="Pesquise por doenças recentes nas últimas 4 semanas nas seguintes cidades no Brasil: {cities}. Concentre-se em reunir dados abrangentes sobre essas doenças, incluindo seus sintomas, propagação e quaisquer medidas em andamento.",
    expected_output='Um relatório detalhado sobre doenças recentes nas cidades especificadas no Brasil.',
    tools=[search_tool],
    agent=researcher,
)

analysis_task = Task(
    description="Analise os dados coletados sobre doenças recentes nas cidades especificadas. Forneça insights sobre as tendências, riscos potenciais e quaisquer recomendações para controle de doenças.",
    expected_output='Um relatório analítico com insights e recomendações baseados nos dados recentes sobre doenças.',
    tools=[exa_search_tool],
    agent=analyst,
)

crew = Crew(
    agents=[researcher, analyst, manager],
    tasks=[search_task, analysis_task],
    Language='pt-br',
    process=Process.sequential 
)

inputs = {'cities': ['São Paulo']}

result = crew.kickoff(inputs=inputs)
print(result)


#     system_template="""
# Você é um pesquisador de IA especializado em identificar e documentar surtos recentes de doenças em locais específicos.
# Sua tarefa é reunir dados sobre doenças nas cidades especificadas no Brasil nas últimas 4 semanas.
# Seja minucioso em sua busca e garanta que os dados sejam abrangentes e precisos.
# """,
#     prompt_template="""
# Sua tarefa é pesquisar doenças recentes nas seguintes cidades: {cities}.
# Concentre-se em encontrar informações abrangentes sobre as doenças, incluindo sintomas, propagação e quaisquer medidas em andamento.
# Garanta que os dados sejam das últimas 4 semanas.
# """,
#     response_template="""
# Aqui está o relatório detalhado sobre as doenças recentes nas cidades especificadas:

# {response}

# Por favor, garanta que os dados sejam precisos e incluam todos os detalhes relevantes sobre as doenças, incluindo sintomas, propagação e medidas em andamento.
# """