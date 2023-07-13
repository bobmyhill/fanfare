from pydub.playback import play
from .aliases import aliases, descriptors
import random
import os


def play_say_and_report(pr_data, tune):
    play(tune)

    author = pr_data["user"]["login"]
    merger = pr_data["merged_by"]["login"]
    additions = pr_data["additions"]

    if author in aliases:
        author = aliases[author]
    if merger in aliases:
        merger = aliases[merger]

    congratulations = (f"Congratulations {author}, "
                       f"{merger} merged your {random.choice(descriptors)} "
                       f"{additions} line pull request")

    try:
        os.system(f"say '{congratulations}'")
    except:
        pass

    print(congratulations)
