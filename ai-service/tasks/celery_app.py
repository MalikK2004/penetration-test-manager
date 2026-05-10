import os
from celery import Celery

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "ai_tasks",
    broker=REDIS_URL,
    backend=REDIS_URL
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

@celery_app.task
def generate_report_task(project_name, finding):
    # This is a stub for the long-running generation task
    from services.groq_client import GroqClient
    from prompts.templates import SYSTEM_PROMPT, REPORT_PROMPT
    
    client = GroqClient()
    user_prompt = REPORT_PROMPT.format(input_data=f"{project_name}: {finding}")
    return client.generate_report(SYSTEM_PROMPT, user_prompt)
