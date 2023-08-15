#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import threading
import os
import sys
from bot import bot


def start_bot():
    bot.infinity_polling()


def start_django():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'financial_bot.settings')
    try:
        from django.core.management import execute_from_command_line

    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'runserver':
        telegram_thread = threading.Thread(target=start_bot)
        telegram_thread.start()
    start_django()

