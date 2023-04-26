"""Module defining functions for logging terminal output."""


def log_critical_error(msg):
    """
    Logs an error message to terminal (in red).

    Parameters:
        msg (str): the error message.
    """
    print(f"\033[91mUnexpected Error: \033[0m{msg}")


def log_error(msg):
    """
    Logs a warning message to terminal (in yellow).

    Parameters:
        msg (str): the error message.
    """
    print(f"\033[93mError: \033[0m{msg}")


def log_success(msg):
    """
    Logs a success message to terminal (in green).

    Parameters:
        msg (str): the error message.
    """
    print(f"\033[92mSuccess: \033[0m{msg}")
