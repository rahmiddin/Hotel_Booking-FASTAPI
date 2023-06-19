from PIL import Image
from pathlib import Path
import smtplib

from pydantic import EmailStr

from app.tasks.celery_task import celery
from app.tasks.email_template import create_booking_confirmation_template
from app.config import settings


@celery.task
def process_pic(
        path: str,
):
    im_path = Path(path)
    im = Image.open(path)
    im_resized = im.resize((1000, 500))
    im_resized2 = im.resize((200, 100))
    im_resized.save(f"app/static/images/resized{im_path.name}")
    im_resized2.save(f"app/static/images/resized2{im_path.name}")


@celery.task
def send_email(
        booking: dict,
        email_to: EmailStr
):
    msg_content = create_booking_confirmation_template(booking, email_to)
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)