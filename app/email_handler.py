import imaplib
import email
from email.header import decode_header
import smtplib
from email.mime.text import MIMEText
import logging
import os

logger = logging.getLogger(__name__)

class EmailHandler:
    def __init__(self):
        self.imap_server = os.getenv('YANDEX_IMAP_SERVER', 'imap.yandex.com')
        self.username = os.getenv('YANDEX_USERNAME')
        self.password = os.getenv('YANDEX_PASSWORD')
        if not self.username or not self.password:
            raise ValueError("Yandex credentials not set in environment variables")

    def check_new_emails(self):
        """Fetch new unread emails from Yandex mailbox."""
        try:
            mail = imaplib.IMAP4_SSL(self.imap_server)
            mail.login(self.username, self.password)
            mail.select('inbox')

            # Search for unread emails
            status, messages = mail.search(None, 'UNSEEN')
            if status != 'OK':
                logger.error("Failed to search emails")
                return []

            email_ids = messages[0].split()
            new_emails = []

            for e_id in email_ids[-10:]:  # Last 10 unread emails
                res, msg = mail.fetch(e_id, '(RFC822)')
                if res != 'OK':
                    continue
                raw_email = msg[0][1]
                email_message = email.message_from_bytes(raw_email)

                subject, encoding = decode_header(email_message["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding or 'utf-8')

                from_email = email_message["From"]

                content = self._get_email_content(email_message)

                new_emails.append({
                    'id': e_id.decode(),
                    'subject': subject,
                    'from_email': from_email,
                    'content': content
                })

            mail.logout()
            return new_emails
        except Exception as e:
            logger.error(f"Error checking emails: {e}")
            return []

    def _get_email_content(self, email_message):
        """Extract plain text content from email."""
        content = ""
        if email_message.is_multipart():
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    content += part.get_payload(decode=True).decode('utf-8', errors='ignore')
        else:
            content = email_message.get_payload(decode=True).decode('utf-8', errors='ignore')
        return content.strip()

    def send_reply(self, to_email, original_subject, response_body):
        """Send a reply email."""
        try:
            msg = MIMEText(response_body)
            msg['Subject'] = f"Re: {original_subject}"
            msg['From'] = self.username
            msg['To'] = to_email

            with smtplib.SMTP_SSL('smtp.yandex.com', 465) as server:
                server.login(self.username, self.password)
                server.send_message(msg)
            logger.info(f"Sent reply email to {to_email}")
        except Exception as e:
            logger.error(f"Failed to send reply email: {e}")