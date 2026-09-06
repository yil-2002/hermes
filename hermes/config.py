import os
from typing import List

class Config:
    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
    WEBHOOK_SECRET = os.getenv("TELEGRAM_WEBHOOK_SECRET", "")
    DOMAIN = os.getenv("HERMES_DOMAIN", "")
    
    ALLOWED_USERS: List[int] = [
        int(x.strip()) for x in os.getenv("HERMES_ALLOWED_USERS", "").split(",") if x.strip()
    ]
    
    DAILY_BUDGET = int(os.getenv("HERMES_DAILY_TOKEN_BUDGET", "0"))
    T1_CONTEXT_TOKENS = int(os.getenv("HERMES_T1_CONTEXT_TOKENS", "64000"))
    DB_PATH = os.getenv("HERMES_DB_PATH", "memory.db")
    MAX_DOC_BYTES = int(os.getenv("HERMES_TELEGRAM_MAX_DOCUMENT_BYTES", str(20*1024*1024)))
