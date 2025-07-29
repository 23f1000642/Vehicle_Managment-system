import os
from celery import Celery
from celery.schedules import crontab
from app import create_app

# Create Flask app
flask_app = create_app()

# Create Celery instance
celery = Celery('parking_app')

# Configure Celery with the same Redis URL as Flask
with flask_app.app_context():
    redis_url = flask_app.config['REDIS_URL']

celery.conf.update(
    broker_url=redis_url,
    result_backend=redis_url,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Kolkata',
    enable_utc=True,
    
    # Scheduled tasks configuration
    beat_schedule={
        'daily-reminder': {
            'task': 'app.tasks.send_daily_reminders',
            'schedule': crontab(hour=18, minute=0),  # 6 PM daily
        },
        'monthly-report': {
            'task': 'app.tasks.send_monthly_reports',
            'schedule': crontab(day_of_month=1, hour=9, minute=0),  # 1st day of month at 9 AM
        },
    },
)

# Task context
class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with flask_app.app_context():
            return self.run(*args, **kwargs)

celery.Task = ContextTask

# Import tasks after celery configuration
from app.tasks import *

if __name__ == '__main__':
    celery.start()