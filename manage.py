#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import time, requests

def view_update():
    while True:
        requests.get("http://127.0.0.1:8000/update")
        # delay one day
        time.sleep(24 * 60 * 60)


def main():
    """Run administrative tasks."""
    # threading.Thread(target=update, args=(), name="get new data").start()
    print("start thread")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_final.settings')
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
    main()
