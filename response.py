"""
This file contains the functions necessary for
creating the interactive response dial at the end of a trial.
To run the 'microsaccade bias colour vs. duration' experiment, see main.py.

made by Anna van Harmelen, 2026
"""

from psychopy import visual, event
from psychopy.hardware.keyboard import Keyboard
from stimuli import (
    draw_fixation_dot,
)
from time import time
from eyetracker import get_trigger


def evaluate_response(key, congruency):
    if key == None:
        correct_response = False
        feedback = "missed"
    elif congruency == "congruent" and key == "up":
        correct_response = True
        feedback = "correct"
    elif congruency == "incongruent" and key == "down":
        correct_response = True
        feedback = "correct"
    else:
        correct_response = False
        feedback = "wrong"

    return {
        "correct_response": correct_response,
        "feedback": feedback,
    }


def get_response(
    stimuli,
    target_duration_cat,
    block_type,
    target_position,
    target_number,
    target_congruency,
    settings,
    testing,
    eyetracker,
):
    keyboard: Keyboard = settings["keyboard"]

    # Check for pressed 'q'
    check_quit(keyboard)

    # Check if _any_ keys were prematurely pressed
    prematurely_pressed = [(key.value, key.rt) for key in keyboard.getKeys()]
    keyboard.clearEvents()

    # Draw fixation object and show response can start
    draw_fixation_dot(stimuli["fixation_dot"], "#000000")
    settings["window"].flip()
    reaction_time_start = time()

    # Wait for response (for max 2 seconds)
    key_pressed = keyboard.waitKeys(keyList=["up", "down", "q"], maxWait=3)

    response_given = time()
    reaction_time = response_given - reaction_time_start

    if not testing and eyetracker and key_pressed:
        trigger = get_trigger(
            "response_given",
            block_type,
            target_position,
            target_duration_cat,
            target_congruency,
            target_number,
        )
        eyetracker.tracker.send_message(f"trig{trigger}")

    # Convert key press to something useful
    key = key_pressed[0].value if key_pressed else None

    # Make sure keystrokes made during this trial don't influence the next
    keyboard.clearEvents()

    return {
        "reaction_time_in_ms": round(reaction_time * 1000, 2),
        "key_pressed": key,
        "premature_pressed": True if prematurely_pressed else False,
        "premature_presses": prematurely_pressed if prematurely_pressed else None,
        **evaluate_response(key, target_congruency),
    }


def wait_for_key(key_list, keyboard):
    keyboard: Keyboard = keyboard
    keyboard.clearEvents()
    keys = keyboard.waitKeys(keyList=key_list)

    return keys


def check_quit(keyboard):
    if keyboard.getKeys("q", clear=False):
        raise KeyboardInterrupt()
