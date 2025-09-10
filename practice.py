"""
This file contains the functions necessary for
practising the trials and the use of the report dial.
To run the 'microsaccade bias colour vs. duration' experiment, see main.py.

made by Anna van Harmelen, 2025
"""

from stimuli import (
    draw_colour_wheel,
    RADIUS_COLOUR_WHEEL as RADIUS,
    INNER_RADIUS_COLOUR_WHEEL as INNER_RADIUS,
    show_text,
)
from response import get_colour_response, wait_for_key
from trial import generate_trial_characteristics, single_trial
from psychopy import event, visual
from time import sleep
import random
from numpy import mean


def practice(settings):
    # Practice response wheel
    practice_colour_wheel(settings)

    # Practice full trials
    practice_trials(settings)


def practice_colour_wheel(settings):
    # Practice response until participant chooses to stop
    try:
        while True:

            # Create square to indicate target colour
            target_colour = random.choice(settings["colours"])
            target_item = visual.Rect(
                settings["window"],
                width=settings["deg2pix"](2),
                height=settings["deg2pix"](2),
                fillColor=target_colour,
                colorSpace="hsv",
            )

            response = get_colour_response(
                target_colour, None, None, None, settings, True, None, [target_item]
            )

            # Give feedback
            target_item.draw()
            visual.TextStim(
                win=settings["window"],
                text=f"{response['performance']}",
                font="Courier New",
                height=22,
                pos=(0, 0),
                color=[-1, -1, -1],
                bold=True,
            ).draw()
            settings["window"].flip()
            sleep(0.5)

    except KeyboardInterrupt:
        show_text(
            "You decided to stop practising the response dial. "
            "Press SPACE to start practicing full trials."
            "\n\nRemember to press Q to stop practising these trials and move on to the final practice part.",
            settings["window"],
        )
        settings["window"].flip()
        wait_for_key(["space"], settings["keyboard"])


def practice_trials(settings):
    # Practice full trials until participant chooses to stop
    try:
        while True:
            target_item = random.choice([1, 2])
            informative_cue = random.choice([True, True, False])
            locs = random.choices(["left", "right"], k=2)

            stimulus = generate_trial_characteristics(
                (target_item, informative_cue, *locs), settings
            )
            report = single_trial(
                **stimulus, settings=settings, testing=True, eyetracker=None
            )

    except KeyboardInterrupt:
        settings["window"].flip()
        show_text(
            "You decided to stop practicing the trials."
            f"\n\nPress SPACE to start the experiment.",
            settings["window"],
        )
        settings["window"].flip()
        wait_for_key(["space"], settings["keyboard"])
