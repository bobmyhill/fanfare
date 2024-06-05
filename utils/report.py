from pydub.playback import play
from .aliases import aliases, descriptors
import random
import os


def play_say_and_report(pr_data, tune):
    """
    Function that plays a tune and says and
    prints data about a pull request.

    Intended to be used for recently merged
    pull requests.

    :param pr_data: Data on the pull request.
    :type pr_data: dict

    :param tune: The tune to play.
    :type tune: pydub.AudioSegment() instance
    """
    play(tune)
    print(pr_data)
    try:
        author = pr_data["user"]["login"]
        merger = pr_data["merged_by"]["login"]
        additions = pr_data["additions"]

        if author in aliases:
            author = aliases[author]
        if merger in aliases:
            merger = aliases[merger]

        congratulations = (
            f"Congratulations {author}, "
            f"{merger} merged your {random.choice(descriptors)} "
            f"{additions} line pull request"
        )

        try:
            os.system(f"say '{congratulations}'")

        except:

            pass

        print(congratulations)

    except TypeError:

        try:
            author = pr_data["user"]["login"]
            additions = pr_data["additions"]

            if author in aliases:
                author = aliases[author]

            commiserations = (
                f"Oh dear {author}, your "
                f"{additions} line pull request was closed without merging. "
                "I wish I had better news for you..."
            )
            os.system(f"say '{commiserations}'")

        except TypeError:
            pass

        pass
