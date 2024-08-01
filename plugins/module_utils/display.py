# Copyright 2024, Itential Inc. All Rights Reserved

# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from ansible.utils.display import Display


display = Display()


def tostring(msg) -> None:
    """Ensures the passed message is a string

    Args:
        msg (str) -> None: The message to display

    Returns:
        None
    """
    return str(msg)


def v(msg, host=None) -> None:
    """Display message to stdout when verbosity is set to 1

    Args:
        msg (str): The message to display
        host (str): The host associated with this message

    Returns:
        None
    """
    display.v(tostring(msg), host)


def vv(msg, host=None) -> None:
    """Display message to stdout when verbosity is set to 2

    Args:
        msg (str): The message to display
        host (str): The host associated with this message

    Returns:
        None
    """
    display.vv(tostring(msg), host)


def vvv(msg, host=None) -> None:
    """Display message to stdout when verbosity is set to 3

    Args:
        msg (str): The message to display
        host (str): The host associated with this message

    Returns:
        None
    """
    display.vvv(tostring(msg), host)


def vvvv(msg, host=None) -> None:
    """Display message to stdout when verbosity is set to 4

    Args:
        msg (str): The message to display
        host (str): The host associated with this message

    Returns:
        None
    """
    display.vvvv(tostring(msg), host)


def vvvvv(msg, host=None) -> None:
    """Display message to stdout when verbosity is set to 5

    Args:
        msg (str): The message to display
        host (str): The host associated with this message

    Returns:
        None
    """
    display.vvvvv(tostring(msg), host)


def vvvvvv(msg, host=None) -> None:
    """Display message to stdout when verbosity is set to 6

    Args:
        msg (str): The message to display
        host (str): The host associated with this message

    Returns:
        None
    """
    display.vvvvvv(tostring(msg), host)


def debug(msg, host=None) -> None:
    """Display message to stdout when debug is enabled

    Args:
        msg (str): The message to display
        host (str): The host associated with this message

    Returns:
        None
    """
    display.debug(tostring(msg), host)


def error(msg, host=None) -> None:
    """Display error message to stdout

    Args:
        msg (str): The message to display
        host (str): The host associated with this message

    Returns:
        None
    """
    display.error(tostring(msg), host)


def warning(msg, host=None) -> None:
    """Display warning message to stdout

    Args:
        msg (str): The message to display
        host (str): The host associated with this message

    Returns:
        None
    """
    display.warning(tostring(msg), host)

def trace(msg, host=None) -> None:
    """Display trace messsages to stdout

    Args:
        msg (str): The message to display
        host (str): The host associated with this message

    Returns:
        None
    """
    display.vvvvv(f"TRACE {msg}", host=host)
