import requests
import json
from datetime import datetime
import subprocess
from urllib3.exceptions import NewConnectionError, MaxRetryError


def get_merged_prs(repo, fields, n_max):
    """
    Use the command line program gh to collect data on merged
    pull requests

    :param repo: The repository in format user/repo
    :type repo: str

    :param fields: A comma-delimited string of the data fields to collect
    :type fields: str

    :param n_max: Maximum number of pull requests for which to collect data
    :type n_max: int

    :returns: Dictionary containing information on the pull requests.
    :rtype: dict
    """
    fields_use = (
        fields.replace("user", "author")
        .replace("merged_at", "mergedAt")
        .replace("merged_by", "mergedBy")
    )
    output = subprocess.check_output(
        f"gh pr list --limit {n_max} --state merged --json {fields_use} --repo {repo}",
        shell=True,
    )
    all_pr_data = json.loads(output)

    d = {d["number"]: d for d in all_pr_data}

    for number in d.keys():
        d[number]["user"] = d[number]["author"]
        d[number]["merged_at"] = d[number]["mergedAt"]
        d[number]["merged_by"] = d[number]["mergedBy"]
        d[number]["merge_time"] = datetime.strptime(
            d[number]["merged_at"], "%Y-%m-%dT%H:%M:%SZ"
        )

    return d


def add_new_pr(repo, number, dict, fields):
    """
    Performs in-place addition of information for a pull request
    to an existing dictionary.

    :param repo: The repository in format user/repo
    :type repo: str

    :param number: The pull request number
    :type number: int

    :rparam dict: Dictionary to which the pull request should be added.
    :type dict: dict

    :param fields: A comma-delimited string of the data fields to collect
    :type fields: str
    """
    api_response = requests.get(f"https://api.github.com/repos/{repo}/pulls/{number}")
    data = json.loads(api_response.text)
    dict[number] = {}
    for field in fields.split(","):
        dict[number][field] = data[field]

    dict[number]["merge_time"] = datetime.strptime(
        dict[number]["merged_at"], "%Y-%m-%dT%H:%M:%SZ"
    )


def get_most_recent_updated_pr(repo, number_with_connection_error=1):
    """
    Gets the number corresponding to the pull request that has been updated
    most recently. This update could be a merge or a comment.

    :param repo: The repository in format user/repo
    :type repo: str

    :param number_with_connection_error: The number to return if there is a connection error.
    :type number_with_connection_error: int

    :returns: The number corresponding to the pull request that has been updated most recently.
    :rtype: int
    """
    try:
        url = (
            f"https://github.com/{repo}/pulls?q=is%3Apr+is%3Aclosed+sort%3Aupdated-desc"
        )
        r = requests.get(url, allow_redirects=True)
        lines = r.content.decode().split("\n")
        index = next((i for i in enumerate(lines) if "     #" in i[1]), [-1, -1])[0]
        return lines[index].split("#")[1]
    except requests.exceptions.ConnectionError or NewConnectionError or MaxRetryError:
        print("No connection")
        return number_with_connection_error
