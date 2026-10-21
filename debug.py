"""
This script is used to test random aspects
of the 'microsaccade bias colour vs. duration' experiment.

made by Anna van Harmelen, 2026
"""

from set_up import get_monitor_and_dir
from set_up import get_settings
from block import long_break

monitor, directory = get_monitor_and_dir(True)
settings = get_settings(monitor, directory)

long_break(12, 100, settings, None)
