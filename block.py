"""
This file contains the functions necessary for
creating and running a full block of trials start-to-finish.
To run the 'microsaccade bias colour vs. duration' experiment, see main.py.

made by Anna van Harmelen, 2026
"""

import random
from stimuli import show_text
from response import wait_for_key
from psychopy import event


def create_trial_list(n_trials):
    if n_trials % 16 != 0:
        raise Exception(
            "Expected number of trials to be divisible by 8, otherwise perfect factorial combinations are not possible."
        )

    # Determine locations counterweighted with durations
    target_position = n_trials // 16 * (8 * ["left"] + 8 * ["right"])

    # Generate equal distribution of stimulus durations
    target_duration = n_trials // 8 * (4 * ["short"] + 4 * ["long"])

    # Determine congruency of final verification target
    target_congruency = n_trials // 4 * (2 * ["congruent"] + 2 * ["incongruent"])

    # Generate equal distribution of target items
    target_item = n_trials // 2 * [1, 2]

    # Create trial parameters for all trials
    trials = list(zip(target_position, target_duration, target_congruency, target_item))
    random.shuffle(trials)

    return trials


def block_break(current_block, n_blocks, avg_score, settings, eyetracker):
    blocks_left = n_blocks - current_block

    break_string = f"In the previous block, you scored {avg_score}% correct."

    show_text(
        break_string
        + f"\n\nYou just finished block {current_block}, you {'only ' if blocks_left == 1 else ''}"
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

    # Make sure keystrokes made during this trial don't influence the next
    settings["keyboard"].clearEvents()

    return False


def long_break(n_blocks, avg_score, settings, eyetracker):
    if n_blocks % 2 == 1:
        odd = " over"
    else:
        odd = ""

    break_string = f"In the previous block, you scored {avg_score}% correct."

    show_text(
        break_string
        + f"\n\nYou're{odd} halfway through! You have {round(n_blocks // 2)} blocks left. "
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

    # Make sure keystrokes made during this trial don't influence the next
    settings["keyboard"].clearEvents()

    return False


def finish(n_blocks, current_session, settings):
    if current_session == 1:
        finish_text = "You're done with the first part now."
    elif current_session == 2:
        finish_text = "You're completely done now!"

    show_text(
        f"Congratulations! You successfully finished all {n_blocks} blocks! "
        + finish_text
        + "\nPress SPACE to exit the experiment.",
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
