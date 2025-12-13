import os


def get_current_directory():
    """
    Get the current working directory.
    :return:
    str: The current working directory.
    """
    return os.getcwd()

def get_current_date():
    """
    Get the current date.
    :return:
    str: The current date in YYYY-MM-DD format.
    """
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d")

def get_current_time():
    """
    Get the current time.
    :return:
    str: The current time in HH:MM:SS format.
    """
    from datetime import datetime
    return datetime.now().strftime("%H:%M:%S")