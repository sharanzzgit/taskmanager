from fastapi_mail import FastMail,MessageSchema,ConnectionConfig
from app.config import settings
import os

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

async def send_task_email(email:str,task_title:str):
    if os.getenv("TESTING")=="1":
        return
    
    message = MessageSchema(
        subject="Task Created",
        recipients=[email],
        body=f"Your task {task_title} has been created successfully.",
        subtype="plain"
    )
    fm = FastMail(conf)
    await fm.send_message(message)