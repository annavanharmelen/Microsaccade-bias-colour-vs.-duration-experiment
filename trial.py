"""
This file contains the functions necessary for
creating and running a single trial start-to-finish,
including eyetracker triggers.
To run the 'microsaccade bias colour vs. duration' experiment, see main.py.

made by Anna van Harmelen, 2025
"""

from psychopy.core import wait
from time import time, sleep
from response import get_colour_response, get_duration_response, check_quit
from stimuli import (
    draw_fixation_dot,
    create_stimuli_frame,
    create_cue_frame,
    show_text,
)
from eyetracker import get_trigger
import random


def generate_trial_characteristics(conditions, settings):
    # Extract condition information
    target_position, target_duration_cat, target_item = conditions

    # Decide on random durations of stimuli
    duration_dict = {
        "short": random.randint(200, 800),
        "long": random.randint(1200, 1800),
    }
    target_duration = duration_dict[target_duration_cat]
    duration_dict.pop(target_duration_cat)

    # Decide on random colours of stimulus
    stimuli_colours = random.sample(settings["colours"], 2)

    # Determine target colour and position
    if target_position == "left":
        target_colour, distractor_colour = stimuli_colours
        item_order = [target_item, 2 if target_item == 1 else 1]
        durations = [target_duration, list(duration_dict.values())[0]]
        duration_cats = [target_duration_cat, list(duration_dict.keys())[0]]

    elif target_position == "right":
        distractor_colour, target_colour = stimuli_colours
        item_order = [2 if target_item == 1 else 1, target_item]
        durations = [list(duration_dict.values())[0], target_duration]
        duration_cats = [list(duration_dict.keys())[0], target_duration_cat]

    else:
        raise Exception(f"Expected 1 or 2, but received {target_item!r}.")

    if target_item == 1:
        item_positions = [
            target_position,
            "left" if target_position == "right" else "right",
        ]
    elif target_item == 2:
        item_positions = [
            "left" if target_position == "right" else "right",
            target_position,
        ]

    return {
        "ITI": random.randint(500, 800),
        "stimuli_colours": stimuli_colours,
        "positions": item_positions,
        "item_orders": item_order,
        "target_number": target_item,
        "target_colour": target_colour,
        "distractor_colour": distractor_colour,
        "target_position": target_position,
        "target_duration": target_duration,
        "target_duration_cat": target_duration_cat,
        "durations": durations,
        "duration_cats": duration_cats,
    }


def do_while_showing(waiting_time, something_to_do, window):
    """
    Show whatever is drawn to the screen for exactly `waiting_time` period,
    while doing `something_to_do` in the mean time.
    """
    window.flip()
    start = time()
    something_to_do()
    wait(waiting_time - (time() - start))


def single_trial(
    ITI,
    stimuli_colours,
    positions,
    item_orders,
    target_number,
    target_colour,
    distractor_colour,
    target_position,
    target_duration,
    target_duration_cat,
    durations,
    duration_cats,
    block_type,
    stimuli,
    settings,
    testing,
    eyetracker=None,
):
    # Initial fixation cross to eliminate jitter caused by for loop
    draw_fixation_dot(stimuli["fixation_dot"], settings)

    screens = [
        (0, lambda: 0 / 0, None),  # initial one to make life easier
        (
            ITI / 1000,
            lambda: draw_fixation_dot(stimuli["fixation_dot"], settings),
            None,
        ),
        (
            durations[0] / 1000,
            lambda: create_stimuli_frame(
                stimuli, stimuli_colours[0], positions[0], settings
            ),
            "stimulus_onset_1",
        ),
        (0.75, lambda: draw_fixation_dot(stimuli["fixation_dot"], settings), None),
        (
            durations[1] / 1000,
            lambda: create_stimuli_frame(
                stimuli, stimuli_colours[1], positions[1], settings
            ),
            "stimulus_onset_2",
        ),
        (0.75, lambda: draw_fixation_dot(stimuli["fixation_dot"], settings), None),
        (
            0.25,
            lambda: create_cue_frame(stimuli, target_number, settings),
            "cue_onset",
        ),
        (1.00, lambda: draw_fixation_dot(stimuli["fixation_dot"], settings), None),
    ]

    # !!! The timing you pass to do_while_showing is the timing for the previously drawn screen. !!!
    for index, (duration, _, frame) in enumerate(screens[:-1]):
        # Send trigger if not testing
        if not testing and frame:
            trigger = get_trigger(
                frame, block_type, target_position, target_duration, target_number
            )
            eyetracker.tracker.send_message(f"trig{trigger}")

        # Check for pressed 'q'
        check_quit(settings["keyboard"])

        # Draw the next screen while showing the current one
        do_while_showing(duration, screens[index + 1][1], settings["window"])

    # The for loop only draws the last frame, never shows it
    # So show it here + wait
    settings["window"].flip()
    wait(screens[-1][0])

    # Let participant respond, type depends on block type
    if block_type == "colour":
        response = get_colour_response(
            stimuli,
            target_colour,
            target_duration,
            block_type,
            target_position,
            target_number,
            settings,
            testing,
            eyetracker,
        )
    elif block_type == "duration":
        response = get_duration_response(
            stimuli,
            target_duration,
            block_type,
            target_position,
            target_number,
            settings,
            testing,
            eyetracker,
        )

    # Show performance
    draw_fixation_dot(stimuli["fixation_dot"], settings)
    show_text(
        f"{response['performance']}", settings["window"], (0, settings["deg2pix"](0.3))
    )

    if not testing:
        trigger = get_trigger(
            "feedback_onset",
            block_type,
            target_position,
            target_duration,
            target_number,
        )
        eyetracker.tracker.send_message(f"trig{trigger}")

    settings["window"].flip()
    sleep(0.25)

    return {
        "condition_code": get_trigger(
            "stimulus_onset_1",
            block_type,
            target_position,
            target_duration,
            target_number,
        ),
        **response,
    }
