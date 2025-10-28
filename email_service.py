import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime
from interfaces import EmailServiceInterface
from logger import setup_logger

class EmailService(EmailServiceInterface):
    def __init__(self, smtp_server: str = "smtp.gmail.com", smtp_port: int = 587):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = os.getenv("SENDER_EMAIL", "your_email@gmail.com")
        self.sender_password = os.getenv("SENDER_PASSWORD", "your_app_password")
        self.logger = setup_logger("EmailService")
    
    def send_post_email(self, post_content: str, topic: str, platform: str, subject_line: str = "", image_url: str = None, recipient_email: str = "pn5513580972@gmail.com") -> bool:
        """Send generated post via email"""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient_email
            msg['Subject'] = f"Generated {platform.title()} Post - {topic}"
            
            # Email body
            subject_text = f"\nSubject Line: {subject_line}\n" if subject_line else ""
            image_text = f"\nImage: {image_url}\n" if image_url else ""
            
            body = f"""
Hello!

Here's your generated {platform.title()} post on the trending topic: {topic}

Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
{subject_text}{image_text}
POST CONTENT:
{'-' * 50}
{post_content}
{'-' * 50}

Platform: {platform.title()}
Topic: {topic}

Best regards,
Homeopathic Health Posts Generator
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            text = msg.as_string()
            server.sendmail(self.sender_email, recipient_email, text)
            server.quit()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Email error: {str(e)}")
            return False
    
    def send_simple_email(self, post_content: str, topic: str, platform: str, subject_line: str = "", image_url: str = None) -> str:
        """Generate mailto link for simple email sending"""
        subject = f"Generated {platform.title()} Post - {topic}"
        subject_text = f"\nSubject Line: {subject_line}\n" if subject_line else ""
        image_text = f"\nImage: {image_url}\n" if image_url else ""
        body = f"Here's your generated {platform.title()} post:{subject_text}{image_text}\n\n{post_content}"
        
        mailto_link = f"mailto:pn5513580972@gmail.com?subject={subject}&body={body}"
        return mailto_link