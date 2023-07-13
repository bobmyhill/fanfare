# fanfare
Uses the GitHub API to play music when a PR is merged.

## Usage
`python ./fanfare.py <github repository> <path to wav file>`

For example:
`python ./fanfare.py geodynamics/aspect ./music/celebrate.wav`

## Requirements
Requires the command line program `gh`, and the python module pydub
`python -m pip install pydub`, and local GitHub authorisation.

On Mac systems, the `say` command line program is also used.