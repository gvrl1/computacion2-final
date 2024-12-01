from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

@app.task
def process_message(message):
    # Simula procesamiento complejo
    return f"Processed: {message}"