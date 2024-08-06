'''
Модуль отправки логов в Telegram
'''
import os

import urllib3
import logging
from datetime import datetime
from logging import LogRecord, Handler
from logging.handlers import RotatingFileHandler

from config import settings


class TelegramBotHandler(Handler):
    def __init__(self):
        super().__init__()
        self.token = settings.TELEGRAM_LOGS_TOKEN
        self.chat_id = settings.TG_CHAT_ID_LOGS

    def emit(self, record: LogRecord) -> None:
        url = f'https://api.telegram.org/bot{self.token}/sendMessage'
        post_data = {'chat_id': self.chat_id,
                     'text': self.format(record)}
        http = urllib3.PoolManager()
        http.request(method='POST', url=url, fields=post_data)


def setup_logging():
    logging.basicConfig(encoding='utf-8', level=logging.INFO)
    logs_path = settings.LOGS_PATH
    if not logs_path:
        logs_path = "logs"
    if not os.path.exists(logs_path):
        os.makedirs(logs_path)

    dt_now = datetime.now().strftime("%Y-%m-%d")
    log_file = f"{logs_path}/{dt_now}_bot.log"
    log_handler = RotatingFileHandler(log_file, maxBytes=1e6, backupCount=5)

    formatter = logging.Formatter('[%(asctime)s -%(msecs)03d] - udacha_bot - %(name)s - %(levelname)7s - %(message)s')
    log_handler.setFormatter(formatter)
    logging.getLogger().addHandler(log_handler)
    # logging.getLogger().addHandler(TelegramBotHandler())

