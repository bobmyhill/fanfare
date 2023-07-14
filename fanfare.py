import time
from pydub import AudioSegment
from utils.github_api import get_merged_prs, add_new_pr
from utils.github_api import get_most_recent_updated_pr
from utils.report import play_say_and_report
import argparse

# User input
parser = argparse.ArgumentParser(
    description="Uses the GitHub API to play music when a PR is merged."
)
parser.add_argument(
    "repo",
    type=str,
    help="the repository of interest in the format user/repo (e.g. geodynamics/aspect)",
)
parser.add_argument(
    "wav_path", type=str, help="the path to the wav file (e.g. ./music/celebrate.wav)"
)

args = parser.parse_args()

repo = args.repo
tune = AudioSegment.from_wav(args.wav_path)

# Get specific fields from the n most recently modified PRs.
# Choose a number n that spans a large enough duration such that
# older PRs probably won't be commented on, but small enough
# that it won't take a ludicrously long time to import.
# 300 is probably a decent number.
fields = "number,title,user,merged_at,merged_by,additions,deletions"
merged_prs = get_merged_prs(repo, fields, 300)
old_pr = get_most_recent_updated_pr(repo, 1)
oldest_time = min([pr["merge_time"] for _, pr in merged_prs.items()])

print(f"Loaded {len(merged_prs)} merged PRs")
# Run a continuous loop for changes to PRs that might represent a merge.
i = 0
while True:
    print(f"Running {i} ({old_pr})")

    new_pr = get_most_recent_updated_pr(repo, old_pr)

    if new_pr != old_pr:
        if new_pr not in merged_prs:
            add_new_pr(repo, new_pr, merged_prs, fields)
            if oldest_time < list(merged_prs.items())[0][1]["merge_time"]:
                play_say_and_report(merged_prs[new_pr], tune)
            else:
                print("This should never happen!")
            old_pr = new_pr

    i += 1
    time.sleep(15)