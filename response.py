"""
This file contains the functions necessary for
creating the interactive response dial at the end of a trial.
To run the 'microsaccade bias colour vs. duration' experiment, see main.py.

made by Anna van Harmelen, 2025
"""

from psychopy import visual, event
from psychopy.hardware.keyboard import Keyboard
from stimuli import (
    draw_colour_wheel,
    draw_fixation_dot,
    draw_item,
    RADIUS_COLOUR_WHEEL as RADIUS,
    INNER_RADIUS_COLOUR_WHEEL as INNER_RADIUS,
)
from time import time
import numpy as np
from eyetracker import get_trigger
import random


def make_marker(radius, inner_radius, settings):
    # Create a marker for the selected colour preview
    marker = visual.Rect(
        settings["window"],
        width=15,
        height=settings["deg2pix"](radius - inner_radius),
        fillColor=None,
        lineColor=(1, 1, 1),
    )

    return marker


def get_colour(mouse_pos, offset, colours):
    # Extract mouse position
    mouse_x, mouse_y = mouse_pos

    # Determine current colour based on mouse position
    angle = (np.degrees(np.arctan2(mouse_y, mouse_x)) + 360) % 360
    colour_angle = angle - offset
    if colour_angle > 360:
        colour_angle -= 360
    current_colour = colours[int(colour_angle)]

    return current_colour, angle


def move_marker(marker, mouse_pos, offset, colours, radius, inner_radius, settings):
    # Get current selected colour and use for marker
    current_colour, angle = get_colour(mouse_pos, offset, colours)
    marker.fillColor = current_colour

    # Fix the marker's position to the colour wheel's radius
    marker.pos = (
        settings["deg2pix"]((radius + inner_radius) / 2 * np.cos(np.radians(angle))),
        settings["deg2pix"]((radius + inner_radius) / 2 * np.sin(np.radians(angle))),
    )

    # Rotate the marker to follow the curve of the donut
    marker.ori = -angle + 90  # Adjust to span across the width of the donut

    marker.draw()

    return current_colour


def evaluate_colour_response(selected_colour, target_colour, colours):
    # Determine position of both colours on colour wheel
    selected_colour_id = colours.index(selected_colour) + 1
    target_colour_id = colours.index(target_colour) + 1

    # Calculate the distance between the two colours
    rgb_distance = selected_colour_id - target_colour_id

    if abs(rgb_distance) > 180:
        abs_rgb_distance = 360 - abs(rgb_distance)
    else:
        abs_rgb_distance = abs(rgb_distance)

    rgb_distance_signed = ((selected_colour_id - target_colour_id + 180) % 360) - 180

    performance = round(100 - abs_rgb_distance / 180 * 100)

    return {
        "rgb_distance": rgb_distance,
        "abs_rgb_distance": abs_rgb_distance,
        "rgb_distance_signed": rgb_distance_signed,
        "performance": performance,
    }


def get_colour_response(
    stimuli,
    target_colour,
    target_duration,
    target_duration_cat,
    block_type,
    target_position,
    target_number,
    settings,
    testing,
    eyetracker,
    additional_objects=[],
):
    mouse = event.Mouse(visible=False, win=settings["window"])
    keyboard: Keyboard = settings["keyboard"]

    # Check for pressed 'q'
    check_quit(keyboard)

    # Check if mouse was prematurely clicked
    _, prematurely_clicked = mouse.getPressed(getTime=True)

    # These timing systems should start at the same time, this is almost true
    mouse.clickReset()
    idle_reaction_time_start = time()

    # Prepare the colour wheel and initialise variables
    offset = random.randint(0, 360)
    mouse.getPos()
    marker = make_marker(RADIUS, INNER_RADIUS, settings)
    marker.colorSpace = "hsv"
    selected_colour = None

    # Wait until participant starts moving the mouse
    while not mouse.mouseMoved():
        # Draw colour wheel
        draw_colour_wheel(stimuli["colour_wheel"], offset, settings)

        # Draw fixation dot
        draw_fixation_dot(stimuli["fixation_dot"], settings)

        # Show additional objects if applicable
        for object in additional_objects:
            object.draw()

        settings["window"].flip()

    response_started = time()
    idle_reaction_time = response_started - idle_reaction_time_start

    if not testing and eyetracker:
        trigger = get_trigger(
            "response_onset",
            block_type,
            target_position,
            target_duration_cat,
            target_number,
        )
        eyetracker.tracker.send_message(f"trig{trigger}")

    # Show colour wheel and get participant response
    while not selected_colour:
        # Check for pressed 'q'
        check_quit(keyboard)

        # Draw colour wheel
        draw_colour_wheel(stimuli["colour_wheel"], offset, settings)

        # Draw fixation dot
        draw_fixation_dot(stimuli["fixation_dot"], settings)

        # Show additional objects if applicable
        for object in additional_objects:
            object.draw()

        # Move the marker
        current_colour = move_marker(
            marker,
            mouse.getPos(),
            offset,
            settings["colours"],
            RADIUS,
            INNER_RADIUS,
            settings,
        )

        # Flip the display
        settings["window"].flip()

        # Check for mouse click
        if mouse.getPressed()[0]:  # Left mouse click
            selected_colour = current_colour

    response_time = time() - response_started

    if not testing and eyetracker:
        trigger = get_trigger(
            "response_offset",
            block_type,
            target_position,
            target_duration_cat,
            target_number,
        )
        eyetracker.tracker.send_message(f"trig{trigger}")

    # Make sure mouse clicks made during this trial don't influence the next
    mouse.clickReset()

    return {
        "idle_reaction_time_in_ms": round(idle_reaction_time * 1000, 2),
        "response_time_in_ms": round(response_time * 1000, 2),
        "premature_pressed": True if prematurely_clicked[0] else False,
        "premature_key": "left_mouse_click" if prematurely_clicked[0] else None,
        "premature_timing": (
            round(prematurely_clicked[0] * 1000, 2) if prematurely_clicked[0] else None
        ),
        "selected_colour": selected_colour,
        "colour_wheel_offset": offset,
        **evaluate_colour_response(selected_colour, target_colour, settings["colours"]),
    }


def evaluate_duration_response(target_duration, response_duration):
    duration_diff = response_duration - target_duration
    duration_diff_abs = abs(duration_diff)
    performance = round(duration_diff)
    sign = "+" if duration_diff > 0 else ""
    return {
        "duration_offset": round(duration_diff),
        "duration_diff_abs": round(duration_diff_abs),
        "performance": f"{sign}{performance}",
    }


def get_duration_response(
    stimuli,
    target_duration,
    target_duration_cat,
    block_type,
    target_position,
    target_number,
    settings,
    testing,
    eyetracker,
):
    mouse = event.Mouse(visible=False, win=settings["window"])
    keyboard: Keyboard = settings["keyboard"]

    # Check for pressed 'q'
    check_quit(keyboard)

    # Show response can start
    draw_fixation_dot(stimuli["fixation_dot"], settings, [-1, -1, -1])
    settings["window"].flip()

    # Check if mouse was prematurely clicked
    _, prematurely_clicked = mouse.getPressed(getTime=True)

    # These timing systems should start at the same time, this is almost true
    mouse.clickReset()
    idle_reaction_time_start = time()

    # Wait for mouse left-click
    clicked = mouse.getPressed()[0]
    while not clicked:
        clicked = mouse.getPressed()[0]
    response_started = time()

    if not testing and eyetracker:
        trigger = get_trigger(
            "response_onset",
            block_type,
            target_position,
            target_duration_cat,
            target_number,
        )
        eyetracker.tracker.send_message(f"trig{trigger}")

    # Show target item while space is held
    while mouse.getPressed()[0]:
        draw_item(stimuli["stimulus"], [0, 0, 1], "middle", settings)
        settings["window"].flip()

    # Compute both reaction times
    response_time = time() - response_started
    idle_reaction_time = response_started - idle_reaction_time_start

    if not testing and eyetracker:
        trigger = get_trigger(
            "response_offset",
            block_type,
            target_position,
            target_duration_cat,
            target_number,
        )
        eyetracker.tracker.send_message(f"trig{trigger}")

    # Make sure mouse clicks made during this trial don't influence the next
    mouse.clickReset()

    return {
        "idle_reaction_time_in_ms": round(idle_reaction_time * 1000, 2),
        "response_time_in_ms": round(response_time * 1000, 2),
        "premature_pressed": True if prematurely_clicked[0] else False,
        "premature_key": "left_mouse_click" if prematurely_clicked[0] else None,
        "premature_timing": (
            round(prematurely_clicked[0] * 1000, 2) if prematurely_clicked[0] else None
        ),
        **evaluate_duration_response(target_duration, response_time * 1000),
    }


def wait_for_key(key_list, keyboard):
    keyboard: Keyboard = keyboard
    keyboard.clearEvents()
    keys = keyboard.waitKeys(keyList=key_list)

    return keys


def check_quit(keyboard):
    if keyboard.getKeys("q"):
        raise KeyboardInterrupt()
