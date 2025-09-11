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
    draw_fixation_dot,
    create_stimulus_frame,
)
from response import (
    get_colour_response,
    wait_for_key,
    check_quit,
    get_duration_response,
)
from trial import generate_trial_characteristics, single_trial
from psychopy import event, visual, core
from time import sleep
import random
from numpy import mean


def practice(block_type, stimuli, settings):
    # Practice relevant block type response
    if block_type == "colour":
        practice_colour_wheel(stimuli, settings)
    elif block_type == "duration":
        practice_duration_response(stimuli, settings)

    # Practice relevant full trials
    practice_trials(block_type, stimuli, settings)


def practice_colour_wheel(stimuli, settings):
    # Practice response until participant chooses to stop
    try:
        performance = []

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
                stimuli,
                target_colour,
                None,
                None,
                None,
                None,
                None,
                settings,
                True,
                None,
                [target_item],
            )

            # Save for post-hoc feedback
            performance.append(int(response["performance"]))

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
        avg_score = round(mean(performance)) if len(performance) > 0 else 0
        
        show_text(
            f"During this practice, your average score was {avg_score}. "
            "\nYou decided to stop practising the response dial. "
            "Press SPACE to start practicing full trials."
            "\n\nRemember to press Q to stop practising these trials and move on to the final practice part.",
            settings["window"],
        )
        settings["window"].flip()
        wait_for_key(["space"], settings["keyboard"])
        
        # Make sure the keystroke from moving to the next part isn't saved
        settings["keyboard"].clearEvents()


def practice_duration_response(stimuli, settings):
    # Practice response until participant chooses to stop
    try:
        performance = []

        # Make sure the keystroke from starting the experiment isn't saved
        settings["keyboard"].clearEvents()

        while True:
            # Show fixation dot in preparation
            draw_fixation_dot(stimuli["fixation_dot"], settings)
            settings["window"].flip()
            sleep(0.5)

            # Show central square with certain duration
            stimulus = generate_trial_characteristics(
                ("left", random.choice(["short", "long"]), 1), settings
            )

            create_stimulus_frame(stimuli, [0,0,1], "middle", settings)
            settings["window"].flip()
            core.wait(stimulus["target_duration"] / 1000)

            # Delay
            draw_fixation_dot(stimuli["fixation_dot"], settings)
            settings["window"].flip()
            core.wait(1.5)

            # Allow response
            report = get_duration_response(
                stimuli,
                stimulus["target_duration"],
                stimulus["target_duration_cat"],
                "duration",
                None,
                None,
                settings,
                True,
                None,
            )

            # Save for post-hoc feedback
            performance.append(int(report["duration_diff_abs"]))

            # Show feedback
            draw_fixation_dot(stimuli["fixation_dot"], settings)
            show_text(
                f"{report['performance']}",
                settings["window"],
                (0, settings["deg2pix"](0.3)),
            )

            if report["premature_pressed"] == True:
                show_text("!", settings["window"], (0, -settings["deg2pix"](0.3)))

            settings["window"].flip()
            sleep(0.25)

            # Pause before next one
            draw_fixation_dot(stimuli["fixation_dot"], settings)
            settings["window"].flip()
            sleep(random.randint(1500, 2000) / 1000)

            # Check for pressed 'q'
            check_quit(settings["keyboard"])

    except KeyboardInterrupt:
        avg_score = round(mean(performance)) if len(performance) > 0 else 0

        show_text(
            f"During this practice, your reports were on average off by {avg_score}. "
            "\nYou decided to stop practising the basic response. "
            "Press SPACE to start practicing full trials."
            "\n\nRemember to press Q to stop practising these trials and move on to the final practice part.",
            settings["window"],
        )
        settings["window"].flip()
        wait_for_key(["space"], settings["keyboard"])

        # Make sure the keystroke from moving to the next part isn't saved
        settings["keyboard"].clearEvents()


def practice_trials(block_type, stimuli, settings):
    # Make sure mouse is invisible
    event.Mouse(visible=False, win=settings["window"])

    # Practice full trials of specific block type until participant chooses to stop
    try:
        while True:
            target_position = random.choice(["left", "right"])
            target_duration = random.choice(["short", "long"])
            target_item = random.choice([1, 2])

            stimulus = generate_trial_characteristics(
                (target_position, target_duration, target_item), settings
            )
            report = single_trial(
                **stimulus,
                block_type=block_type,
                stimuli=stimuli,
                settings=settings,
                testing=True,
                eyetracker=None,
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

        # Make sure the keystroke from moving to the next part isn't saved
        settings["keyboard"].clearEvents()
