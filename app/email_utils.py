import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


def send_lead_notification(name: str, email: str, phone: str, service: str, budget: str, message: str) -> bool:
    """
    Send an email notification to the agency when a new lead submits the contact form.
    Returns True if sent successfully, False otherwise (non-blocking).
    """
    if not all([settings.SMTP_HOST, settings.SMTP_USER, settings.SMTP_PASSWORD, settings.NOTIFICATION_EMAIL]):
        logger.info("Email not configured — skipping notification. Set SMTP_* vars in .env to enable.")
        return False

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"🔥 New Lead from {name} — Sai Creator"
        msg["From"] = settings.SMTP_USER
        msg["To"] = settings.NOTIFICATION_EMAIL

        html_body = f"""
        <!DOCTYPE html>
        <html>
        <body style="font-family: Inter, sans-serif; background: #f9f9f8; padding: 40px 20px;">
          <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 16px;
                      border: 1px solid #e2e2e2; overflow: hidden;">
            <div style="background: #000; padding: 32px; text-align: center;">
              <h1 style="color: white; margin: 0; font-size: 24px;">🔥 New Lead!</h1>
              <p style="color: rgba(255,255,255,0.6); margin: 8px 0 0; font-size: 14px;">
                Someone submitted the contact form on Sai Creator
              </p>
            </div>
            <div style="padding: 32px;">
              <table style="width: 100%; border-collapse: collapse;">
                <tr><td style="padding: 12px 0; border-bottom: 1px solid #f3f4f3; color: #76777d; width: 120px;">Name</td>
                    <td style="padding: 12px 0; border-bottom: 1px solid #f3f4f3; font-weight: 600;">{name}</td></tr>
                <tr><td style="padding: 12px 0; border-bottom: 1px solid #f3f4f3; color: #76777d;">Email</td>
                    <td style="padding: 12px 0; border-bottom: 1px solid #f3f4f3;">
                      <a href="mailto:{email}" style="color: #9d4300;">{email}</a></td></tr>
                <tr><td style="padding: 12px 0; border-bottom: 1px solid #f3f4f3; color: #76777d;">Phone</td>
                    <td style="padding: 12px 0; border-bottom: 1px solid #f3f4f3;">{phone or "—"}</td></tr>
                <tr><td style="padding: 12px 0; border-bottom: 1px solid #f3f4f3; color: #76777d;">Service</td>
                    <td style="padding: 12px 0; border-bottom: 1px solid #f3f4f3;">{service or "—"}</td></tr>
                <tr><td style="padding: 12px 0; border-bottom: 1px solid #f3f4f3; color: #76777d;">Budget</td>
                    <td style="padding: 12px 0; border-bottom: 1px solid #f3f4f3;">{budget or "—"}</td></tr>
              </table>
              <div style="margin-top: 24px; background: #f3f4f3; padding: 20px; border-radius: 12px;">
                <p style="margin: 0 0 8px; color: #76777d; font-size: 12px; text-transform: uppercase; letter-spacing: 0.05em;">Message</p>
                <p style="margin: 0; line-height: 1.6;">{message}</p>
              </div>
              <div style="margin-top: 32px; text-align: center;">
                <a href="{settings.NOTIFICATION_EMAIL}" style="background: #000; color: white; padding: 14px 32px;
                   border-radius: 100px; text-decoration: none; font-weight: 600; font-size: 14px;">
                  View All Leads in Admin
                </a>
              </div>
            </div>
          </div>
        </body>
        </html>
        """

        msg.attach(MIMEText(html_body, "html"))

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(settings.SMTP_USER, settings.NOTIFICATION_EMAIL, msg.as_string())

        logger.info(f"Lead notification email sent for {email}")
        return True

    except Exception as e:
        logger.error(f"Failed to send lead notification: {e}")
        return False
