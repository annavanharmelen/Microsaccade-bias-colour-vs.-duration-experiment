"""
This file contains the functions necessary for
creating the fixation cross and the bar stimuli.
To run the 'microsaccade bias colour vs. duration' experiment, see main.py.

made by Anna van Harmelen, 2025
"""

from psychopy import visual
import numpy as np

DOT_SIZE = 0.1  # radius of fixation dot
ITEM_SIZE = 1  # radius of item
ITEM_ECCENTRICITY = 6.5  # distance from fixation to item

RADIUS_COLOUR_WHEEL = 6
INNER_RADIUS_COLOUR_WHEEL = 4.5


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

    # Create colour wheel
    radius = settings["deg2pix"](RADIUS_COLOUR_WHEEL)
    inner_radius = settings["deg2pix"](INNER_RADIUS_COLOUR_WHEEL)
    num_segments = settings["num_segments"]
    colour_wheel = []

    for i in range(num_segments):
        # Create a wedge for each segment
        verts = [
            [
                inner_radius * np.cos(np.radians(i)),
                inner_radius * np.sin(np.radians(i)),
            ],
            [
                radius * np.cos(np.radians(i)),
                radius * np.sin(np.radians(i)),
            ],
            [
                radius * np.cos(np.radians(i + 1)),
                radius * np.sin(np.radians(i + 1)),
            ],
            [
                inner_radius * np.cos(np.radians(i + 1)),
                inner_radius * np.sin(np.radians(i + 1)),
            ],
        ]

        wedge = visual.ShapeStim(
            settings["window"],
            vertices=verts,
            fillColor=settings["colours"][i],
            lineColor=None,
            colorSpace="hsv",
        )
        colour_wheel.append((wedge, verts))

    return {
        "fixation_dot": fixation_dot,
        "stimulus": stimulus,
        "colour_wheel": colour_wheel,
    }


def draw_fixation_dot(dot, settings, colour="#eaeaea"):
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


def draw_colour_wheel(colour_wheel, offset, settings):
    # Individually turn, move and draw each wedge so the colour wheel matches the desired offset
    angle = np.deg2rad(offset)
    rot = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])

    for wedge, verts in colour_wheel:
        wedge.vertices = verts @ rot.T
        wedge.draw()

    return colour_wheel


def show_text(input, window, pos=(0, 0), colour="#ffffff"):
    textstim = visual.TextStim(
        win=window, font="Courier New", text=input, color=colour, pos=pos, height=22
    )

    textstim.draw()


def create_stimulus_frame(stimuli, colour, position, settings, fix_colour="#eaeaea"):
    draw_fixation_dot(stimuli["fixation_dot"], settings, fix_colour)
    draw_item(stimuli["stimulus"], colour, position, settings)


def create_cue_frame(stimuli, target_item, settings):
    draw_fixation_dot(stimuli["fixation_dot"], settings)
    show_text(target_item, settings["window"], pos=(0, settings["deg2pix"](0.3)))
