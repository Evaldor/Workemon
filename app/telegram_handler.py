import telebot
import threading
import logging
import os

logger = logging.getLogger(__name__)

class TelegramHandler:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not self.token:
            raise ValueError("Telegram bot token not set")
        self.bot = telebot.TeleBot(self.token)
        self.new_messages = []
        self.thread = None

        @self.bot.message_handler(func=lambda message: True)
        def handle_message(message):
            self.new_messages.append({
                'chat_id': message.chat.id,
                'content': message.text
            })
            logger.info(f"Received Telegram message from {message.chat.id}: {message.text}")

    def start_polling(self):
        """Start polling in a background thread."""
        def polling():
            try:
                self.bot.polling(none_stop=True, interval=0)
            except Exception as e:
                logger.error(f"Telegram polling error: {e}")

        self.thread = threading.Thread(target=polling, daemon=True)
        self.thread.start()

    def get_new_messages(self):
        """Get and clear new messages."""
        messages = self.new_messages.copy()
        self.new_messages.clear()
        return messages

    def send_message(self, chat_id, text):
        """Send message to a chat."""
        try:
            self.bot.send_message(chat_id, text)
        except Exception as e:
            logger.error(f"Error sending Telegram message: {e}")