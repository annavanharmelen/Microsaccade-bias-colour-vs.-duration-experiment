"""
This file contains the functions necessary for
practising the trials and the use of the report dial.
To run the 'microsaccade bias colour vs. duration' experiment, see main.py.

made by Anna van Harmelen, 2026
"""

from stimuli import show_text
from response import wait_for_key
from trial import generate_trial_characteristics, single_trial
import random
from numpy import mean


def practice(block_type, stimuli, eyetracker, settings):
    # Practice full trials of specific block type until participant chooses to stop
    try:
        # Show first screen
        show_text(
            "Welcome! "
            + "\nPress SPACE to start practicing the task.",
            settings["window"],
        )
        settings["window"].flip()
        if eyetracker:
            keys = wait_for_key(["space", "c"], settings["keyboard"])
            if "c" in keys:
                eyetracker.calibrate()
                eyetracker.start()
                return True
        else:
            wait_for_key(["space"], settings["keyboard"])

        # Make sure the keystroke from starting the experiment isn't saved
        settings["keyboard"].clearEvents()
        
        # Create empty frame to save performance to
        performance = []

        # Loop until participant chooses to stop practising
        while True:
            target_position = random.choice(["left", "right"])
            target_duration = random.choice(["short", "long"])
            target_congruency = random.choice(["congruent", "incongruent"])
            target_item = random.choice([1, 2])

            stimulus = generate_trial_characteristics(
                (target_position, target_duration, target_congruency, target_item),
                settings,
            )
            report = single_trial(
                **stimulus,
                block_type=block_type,
                stimuli=stimuli,
                settings=settings,
                testing=True,
                eyetracker=None,
            )

            # Save for post-hoc feedback
            performance.append(report["correct_response"])

    except KeyboardInterrupt:
        settings["window"].flip()

        avg_score = round(mean(performance) * 100) if len(performance) > 0 else 0

        break_string = f"\nIn the previous block, you scored {avg_score}% correct."

        show_text(
            "You decided to stop practicing the trials."
            + break_string
            + f"\n\nPress SPACE to start the experiment.",
            settings["window"],
        )
        settings["window"].flip()
        if eyetracker:
            keys = wait_for_key(["space", "c"], settings["keyboard"])
            if "c" in keys:
                eyetracker.calibrate()
                eyetracker.start()
                return True
        else:
            wait_for_key(["space"], settings["keyboard"])

        # Make sure keystrokes made during this trial don't influence the next
        settings["keyboard"].clearEvents()
