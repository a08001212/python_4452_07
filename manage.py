#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import threading
import time, requests, datetime

def view_update()->None:
    # waiting for django start website
    print("In threading")
    time.sleep(5)
    while True:
        # not weekend
        if datetime.date.today().weekday() != 5 and datetime.date.today().weekday() != 6:
            requests.get("http://127.0.0.1:8000/update")
        # waiting for one day
        time.sleep(24 * 60 * 60)



def main():
    """Run administrative tasks."""
    # threading.Thread(target=update, args=(), name="get new data").start()
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


th = threading.Thread(target=view_update,  name="every_day_update_data")
print("start thread")
th.start()

if __name__ == '__main__':

    main()
