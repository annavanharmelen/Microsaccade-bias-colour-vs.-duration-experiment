"""
This file contains the functions necessary for
creating the fixation cross and the bar stimuli.
To run the 'microsaccade bias colour vs. duration' experiment, see main.py.

made by Anna van Harmelen, 2026
"""

from psychopy import visual
import numpy as np
from psychopy.core import wait

DOT_SIZE = 0.1  # radius of fixation dot
ITEM_SIZE = 1  # radius of item
ITEM_ECCENTRICITY = 6.5  # distance from fixation to item


def initialise_all_stimuli(settings):
    # Create fixation dot
    fixation_dot = visual.Circle(
        win=settings["window"],
        units="pix",
        radius=settings["deg2pix"](DOT_SIZE),
        pos=(0, 0),
    )

    # Create main stimulus
    stimulus = visual.Circle(
        win=settings["window"],
        units="pix",
        radius=settings["deg2pix"](ITEM_SIZE),
        colorSpace="hsv",
    )

    return {
        "fixation_dot": fixation_dot,
        "stimulus": stimulus,
    }


def draw_fixation_dot(dot, colour="#eaeaea"):
    dot.setColor(colour)
    dot.draw()


def draw_item(item, colour, position, settings):
    # Parse input
    if position == "left":
        pos = (-settings["deg2pix"](ITEM_ECCENTRICITY), 0)
    elif position == "right":
        pos = (settings["deg2pix"](ITEM_ECCENTRICITY), 0)
    elif position == "middle":
        pos = (0, 0)
    else:
        raise Exception(
            f"Expected 'left', 'right' or 'middle', but received {position!r}."
        )

    # Draw stimulus
    item.pos = pos
    item.setColor(colour, colorSpace="hsv")
    item.draw()


def show_text(input, window, pos=(0, 0), colour="#ffffff"):
    textstim = visual.TextStim(
        win=window, font="Aptos", text=input, color=colour, pos=pos, height=22
    )

    textstim.draw()


def create_stimulus_frame(stimuli, colour, position, settings, fix_colour="#eaeaea"):
    draw_fixation_dot(stimuli["fixation_dot"], fix_colour)
    draw_item(stimuli["stimulus"], colour, position, settings)


def create_cue_frame(stimuli, target_item, settings):
    draw_fixation_dot(stimuli["fixation_dot"])
    show_text(target_item, settings["window"], pos=(0, settings["deg2pix"](0.3)))


def run_verification_frame(block_type, stimuli, duration, colour, settings, testing, eyetracker, trigger):
    # Remove one aspect from stimulus, depending on block type
    if block_type == "colour":
        duration = 500
    elif block_type == "duration":
        colour = "#eaeaea"

    # draw stimulus
    create_stimulus_frame(stimuli, colour, "middle", settings)

    # flip window to show stimulus
    settings["window"].flip()

    # send trigger that stimulus has been shown
    if not testing and eyetracker:
        trigger = trigger
        eyetracker.tracker.send_message(f"trig{trigger}")

    # wait for given duration to stop showing stimulus
    wait(duration / 1000)
