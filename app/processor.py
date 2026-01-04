from .llm_handler import LLMHandler
from .jira_handler import JiraHandler
from .email_handler import EmailHandler
from .telegram_handler import TelegramHandler
from .database import SessionLocal, RequestResponse
import os
import logging

logger = logging.getLogger(__name__)

class Processor:
    def __init__(self):
        self.llm = LLMHandler()
        self.jira = JiraHandler()
        self.email = EmailHandler()
        self.telegram = TelegramHandler()
        self.saved_prompt = os.getenv('SAVED_PROMPT', 'Process this request:')

    def process(self, source, content, extra=None):
        """Process content with LLM and handle response based on source."""
        full_prompt = f"{self.saved_prompt} {content}"
        llm_response = self.llm.call_llm(full_prompt)

        # Save to DB
        db = SessionLocal()
        record = RequestResponse(
            source=source,
            content=content,
            prompt=full_prompt,
            llm_response=llm_response
        )
        db.add(record)
        db.commit()
        db.close()

        # Send response
        if source == 'email':
            # extra = {'to': from_email, 'subject': subject}
            self.email.send_reply(extra['to'], extra['subject'], llm_response)
        elif source == 'telegram':
            # extra = chat_id
            self.telegram.send_message(extra, llm_response)
        elif source == 'api':
            # TODO
            return llm_response
        else:
            self.jira.create_issue("LLM Response", llm_response)