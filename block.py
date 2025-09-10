"""
This file contains the functions necessary for
creating and running a full block of trials start-to-finish.
To run the 'microsaccade bias colour vs. duration' experiment, see main.py.

made by Anna van Harmelen, 2025
"""

import random
from stimuli import show_text
from response import wait_for_key


def create_block_list(n_blocks, start_type):
    if n_blocks % 2 != 0:
        raise Exception(
            "Expected number of blocks to be divisible by 2, otherwise both block types cannot occur equally often."
        )

    return n_blocks // 2 * [start_type] + n_blocks // 2 * [
        "colour" if start_type == "duration" else "duration"
    ]


def create_trial_list(n_trials):
    if n_trials % 8 != 0:
        raise Exception(
            "Expected number of trials to be divisible by 8, otherwise perfect factorial combinations are not possible."
        )

    # Generate equal distribution of target items
    target_item = n_trials // 2 * [1, 2]

    # Generate equal distribution of stimulus durations
    target_duration = n_trials // 4 * (2 * ["short"] + 2 * ["long"])

    # Determine locations counterweighted with durations
    target_position = n_trials // 2 * (4 * ["left"] + 4 * ["right"])

    # Create trial parameters for all trials
    trials = list(zip(target_position, target_duration, target_item))
    random.shuffle(trials)

    return trials


def block_break(current_block, n_blocks, block_type, avg_score, settings, eyetracker):
    blocks_left = n_blocks - current_block

    show_text(
        f"You scored {avg_score}% correct on the previous block. "
        f"\n\nYou just finished block {current_block}, you {'only ' if blocks_left == 1 else ''}"
        f"have {blocks_left} block{'s' if blocks_left != 1 else ''} left. "
        "Take a break if you want to, but try not to move your head during this break."
        "\n\nPress SPACE when you're ready to continue.",
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

    return False


def long_break(n_blocks, block_type, avg_score, settings, eyetracker):
    show_text(
        f"You scored {avg_score}% correct on the previous block. "
        f"\n\nYou're halfway through! You have {n_blocks // 2} blocks left. "
        "Now is the time to take a longer break. Maybe get up, stretch, walk around."
        "\n\nPress SPACE whenever you're ready to continue again.",
        settings["window"],
    )
    settings["window"].flip()

    if eyetracker:
        keys = wait_for_key(["space", "c"], settings["keyboard"])
        if "c" in keys:
            eyetracker.calibrate()
            return True
    else:
        wait_for_key(["space"], settings["keyboard"])

    # Make sure the keystroke from starting the experiment isn't saved
    settings["keyboard"].clearEvents()

    return False


def finish(n_blocks, settings):
    show_text(
        f"Congratulations! You successfully finished all {n_blocks} blocks!"
        "You're completely done now. Press SPACE to exit the experiment.",
        settings["window"],
    )
    settings["window"].flip()

    wait_for_key(["space"], settings["keyboard"])


def quick_finish(settings):
    settings["window"].flip()
    show_text(
        f"You've exited the experiment. Press SPACE to close this window.",
        settings["window"],
    )
    settings["window"].flip()

    wait_for_key(["space"], settings["keyboard"])
