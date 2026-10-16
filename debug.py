"""
This script is used to test random aspects
of the 'microsaccade bias colour vs. duration' experiment.

made by Anna van Harmelen, 2026
"""

from eyetracker import get_trigger

print(get_trigger("response_given", "duration", "right", "short", "incongruent", 1))
