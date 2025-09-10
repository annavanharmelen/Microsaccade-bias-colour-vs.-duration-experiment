"""
This file contains the functions necessary for
collecting participant data.
To run the 'microsaccade bias colour vs. duration' experiment, see main.py.

made by Anna van Harmelen, 2025
"""

import random
import pandas as pd


def get_participant_details(existing_participants: pd.DataFrame, testing):
    # Generate random & unique participant number
    participant = random.randint(10, 99)
    while participant in existing_participants.participant_number.tolist():
        participant = random.randint(10, 99)

    print(f"Participant number: {participant}")

    if not testing:
        # Get participant age
        age = int(input("Participant age: "))
    else:
        age = 00

    # Insert session number
    session = max(existing_participants.session_number) + 1

    # Determine starting block type
    options = ["colour", "duration"]
    previous_start_block_type = existing_participants.start_block_type.tolist()[-1]
    if previous_start_block_type == "0":
        start_block_type = options[0]
    else:
        idx = (options.index(previous_start_block_type) + 1) % len(options)
        start_block_type = options[idx]

    # Add newly made participant
    new_participant = pd.DataFrame(
        {
            "age": [age],
            "participant_number": [participant],
            "session_number": [session],
            "start_block_type": [start_block_type],
        }
    )
    all_participants = pd.concat(
        [existing_participants, new_participant], ignore_index=True
    )

    return all_participants, start_block_type
