"""
This script is used to test random aspects
of the 'microsaccade bias colour vs. duration' experiment.

made by Anna van Harmelen, 2025
"""

from set_up import get_settings
from psychopy import visual, event
import numpy as np
from response import evaluate_colour_response
from block import create_trial_list
from trial import generate_trial_characteristics
import random

my_list = [(1, 2), (3, 4), (5, 6)]
for a, b in my_list:
    print(a)
    print(b)

import sys

sys.exit()

testing = True

monitor = {
    "resolution": (1920, 1080),  # in pixels
    "Hz": 60,  # screen refresh rate in Hz
    "width": 33,  # in cm
    "distance": 50,  # in cm
}

directory = r"../../Data/test/"
settings = get_settings(monitor, directory)

my_list = random.sample(settings["colours"], 2)
a, b = my_list


trials = create_trial_list(16)
print(trials[:2])

print(generate_trial_characteristics(("right", "long", 1), settings))


# Parameters for the color wheel
num_segments = 360  # Number of segments in the wheel (degrees of hue)
radius = 300  # Radius of the color wheel
inner_radius = 200  # Inner radius of the color wheel

# Generate colors for the wheel
colors = [
    [
        np.cos(np.radians(hue)) * 0.5 + 0.5,  # Red channel
        np.cos(np.radians(hue - 120)) * 0.5 + 0.5,  # Green channel
        np.cos(np.radians(hue - 240)) * 0.5 + 0.5,  # Blue channel
    ]
    for hue in range(num_segments)
]

# Draw the color wheel using shapes
color_wheel = []
for i in range(num_segments):
    # Create a wedge for each segment
    wedge = visual.ShapeStim(
        settings["window"],
        vertices=[
            [
                inner_radius * np.cos(np.radians(i)),
                inner_radius * np.sin(np.radians(i)),
            ],
            [radius * np.cos(np.radians(i)), radius * np.sin(np.radians(i))],
            [radius * np.cos(np.radians(i + 1)), radius * np.sin(np.radians(i + 1))],
            [
                inner_radius * np.cos(np.radians(i + 1)),
                inner_radius * np.sin(np.radians(i + 1)),
            ],
        ],
        fillColor=colors[i],
        lineColor=None,
    )
    color_wheel.append(wedge)

# Instruction text
instruction = visual.TextStim(
    settings["window"],
    text="Move the mouse to preview a color, click to select it",
    pos=(0, -250),
    color=(-1, -1, -1),
)

# Create a marker for the selected color preview
marker = visual.Rect(
    settings["window"],
    width=15,
    height=(radius - inner_radius),
    fillColor=None,
    lineColor=(1, 1, 1),
)

# wait until mouse is moved
mouse = event.Mouse(visible=False, win=settings["window"])
mouse.getPos()
while not mouse.mouseMoved():
    settings["window"].flip()

# Draw the color wheel and get user response
selected_color = None
while not selected_color:
    # Draw each wedge
    for wedge in color_wheel:
        wedge.draw()

    # Get mouse position
    mouse_x, mouse_y = mouse.getPos()

    # Calculate the angle corresponding to the mouse's x position
    angle = (np.degrees(np.arctan2(mouse_y, mouse_x)) + 360) % 360
    current_color = colors[int(angle)]
    marker.fillColor = current_color

    # Fix the marker's position to the color wheel's radius
    marker.pos = (
        (radius + inner_radius) / 2 * np.cos(np.radians(angle)),
        (radius + inner_radius) / 2 * np.sin(np.radians(angle)),
    )

    # Rotate the marker to follow the curve of the donut
    marker.ori = -angle + 90  # Adjust to span across the width of the donut

    marker.draw()

    # Draw the instruction text
    instruction.draw()

    # Flip the display
    settings["window"].flip()

    # Check for mouse click
    if mouse.getPressed()[0]:  # Left mouse click
        selected_color = current_color

# Close the window
settings["window"].close()

# Evaluate the response
print(evaluate_colour_response(selected_color, colors[0], colors))
