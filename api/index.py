"""
Vercel serverless entry point — no database, email-only contact form.
"""
import json
import logging
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from http.server import BaseHTTPRequestHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def send_email(name: str, email: str, phone: str, service: str, budget: str, message: str) -> bool:
    """Send lead notification via SMTP. Returns True on success."""
    smtp_host = os.environ.get("SMTP_HOST", "")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    smtp_user = os.environ.get("SMTP_USER", "")
    smtp_pass = os.environ.get("SMTP_PASSWORD", "")
    notify_email = os.environ.get("NOTIFICATION_EMAIL", "")

    if not all([smtp_host, smtp_user, smtp_pass, notify_email]):
        logger.info("Email not configured — skipping. Set SMTP_* env vars in Vercel dashboard.")
        return False

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"🔥 New Lead from {name} — Sai Creations"
        msg["From"] = smtp_user
        msg["To"] = notify_email

        html_body = f"""
        <!DOCTYPE html>
        <html>
        <body style="font-family: Inter, sans-serif; background: #f9f9f8; padding: 40px 20px;">
          <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 16px;
                      border: 1px solid #e2e2e2; overflow: hidden;">
            <div style="background: #000; padding: 32px; text-align: center;">
              <h1 style="color: white; margin: 0; font-size: 24px;">🔥 New Lead!</h1>
              <p style="color: rgba(255,255,255,0.6); margin: 8px 0 0; font-size: 14px;">
                Someone submitted the contact form on Sai Creations
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
            </div>
          </div>
        </body>
        </html>
        """

        msg.attach(MIMEText(html_body, "html"))
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_user, notify_email, msg.as_string())

        logger.info(f"Lead notification email sent for {email}")
        return True

    except Exception as e:
        logger.error(f"Failed to send lead notification: {e}")
        return False


class handler(BaseHTTPRequestHandler):
    """
    Vercel Python serverless handler.
    Handles POST /api/contact and GET /api/health.
    """

    def log_message(self, format, *args):
        logger.info(format % args)

    def _send_json(self, status: int, body: dict):
        payload = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(payload)

    def do_OPTIONS(self):
        """Handle CORS preflight."""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        if self.path == "/api/health" or self.path.startswith("/api/health?"):
            self._send_json(200, {"status": "ok", "app": "Sai Creations"})
        else:
            self._send_json(404, {"detail": "Not found"})

    def do_POST(self):
        if self.path == "/api/contact" or self.path.startswith("/api/contact?"):
            content_length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(content_length)
            try:
                data = json.loads(raw)
            except (json.JSONDecodeError, ValueError):
                self._send_json(400, {"detail": "Invalid JSON"})
                return

            # Validate required fields
            name = (data.get("name") or "").strip()
            email = (data.get("email") or "").strip()
            message = (data.get("message") or "").strip()

            if not name or not email or not message:
                self._send_json(422, {"detail": "name, email, and message are required"})
                return

            phone = (data.get("phone") or "").strip()
            service = (data.get("service") or "").strip()
            budget = (data.get("budget") or "").strip()

            # Send notification email (non-blocking in serverless context)
            send_email(name, email, phone, service, budget, message)

            self._send_json(201, {
                "success": True,
                "message": "Thanks! We'll be in touch within 24 hours."
            })
        else:
            self._send_json(404, {"detail": "Not found"})
