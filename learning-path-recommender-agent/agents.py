from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI  # ya Groq/ChatOllama
from utils import retrieve_courses
import os

# LLM setup (change to Ollama for local)
llm = ChatOpenAI(model="gpt-3.5-turbo")  # ya Groq: model="llama3-8b-8192"

profiler = Agent(
    role='Learner Profiler',
    goal='Analyze learner skills, goals, time, style and create profile summary',
    backstory='Expert educational consultant',
    llm=llm,
    verbose=True
)

analyzer = Agent(
    role='Course Analyzer',
    goal='Retrieve relevant courses and identify gaps/prerequisites',
    backstory='Data scientist specializing in semantic search',
    llm=llm,
    verbose=True
)

planner = Agent(
    role='Learning Path Planner',
    goal='Create optimal sequenced roadmap considering difficulty, time, prerequisites',
    backstory='Senior curriculum designer',
    llm=llm,
    verbose=True
)

def create_crew(profile_text, progress=""):
    retrieve_tool = lambda query: retrieve_courses(query + " " + progress)
    
    task1 = Task(
        description=f"Create detailed learner profile from: {profile_text}",
        expected_output="Structured profile with skill gaps",
        agent=profiler
    )
    
    task2 = Task(
        description="Using retrieved courses, analyze relevance and prerequisites",
        expected_output="List of candidate courses with gap analysis",
        agent=analyzer,
        context=[task1]
    )
    
    task3 = Task(
        description="Build sequenced learning path with estimated weeks, difficulty progression, and alternatives",
        expected_output="JSON formatted roadmap with weekly breakdown",
        agent=planner,
        context=[task2]
    )
    
    crew = Crew(
        agents=[profiler, analyzer, planner],
        tasks=[task1, task2, task3],
        process=Process.sequential,
        verbose=2
    )
    return crew