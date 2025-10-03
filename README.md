# MICROSACCADE BIAS COLOUR VS. DURATION EXPERIMENT
# ***[work in progress]***
A colour and duration reproduction task, designed to measure microsaccade bias in working memory, programmed in Python.

## Author
Made by Anna van Harmelen in 2025, based on own earlier code, see: [Microsaccade bias duration experiment](https://github.com/annavanharmelen/Microsaccade-bias-duration-experiment) and [Microsaccade bias temporal separation experiment](https://github.com/annavanharmelen/Microsaccade-bias-temporal-separation-experiment).

## Installation
This experiment was created using the [PsychoPy library](https://www.psychopy.org), e.g. follow [these instructions](https://www.psychopy.org/download.html).

Additionally, you must also install the [EyeLink developer kit](https://www.sr-research.com/support/thread-13.html).

Then, you must install the PyLink library, using [these instructions](https://www.sr-research.com/support/thread-48.html).
To install using pip:

```
pip install --index-url=https://pypi.sr-support.com sr-research-pylink
```

## Configuration
To make sure the experiment runs correctly, open the set_up.py file to enter the correct specifications of your monitor and set-up on lines 17-37.

## Running
The experiment runs in its entirety (including some explanation, practice trials and breaks) if you run `python main.py`.
Note: this experiment consists of two sessions. Simply run the main experiment twice per participant, and it will automatically run the two different sessions and save the data separately. 
