import os
BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    raise ValueError("Необходимо установить переменную окружения BOT_TOKEN")