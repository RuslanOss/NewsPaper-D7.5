import logging

from django.conf import settings

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.dispatch import Signal

logger = logging.getLogger(__name__)

its_time = Signal()


def weekly_job():
    its_time.send_robust(sender='Weekly')


def delete_old_job_executions(max_age=60*60*24*7):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


def run():
    scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
    scheduler.add_jobstore(DjangoJobStore(), "default")

    scheduler.add_job(
        weekly_job,
        trigger=CronTrigger(day="*/7"),

        id="weekly_job",
        max_instances=1,
        replace_existing=True,
    )
    logger.info("Added job 'weekly_job'.")

    scheduler.add_job(
        delete_old_job_executions,
        trigger=CronTrigger(
            day_of_week="mon", hour="00", minute="00"
        ),

        id="delete_old_job_executions",
        max_instances=1,
        replace_existing=True,
    )
    logger.info(
        "Added weekly job: 'delete_old_job_executions'."
    )

    try:
        logger.info("Starting scheduler...")
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("Stopping scheduler...")
        scheduler.shutdown()
        logger.info("Scheduler shut down successfully!")