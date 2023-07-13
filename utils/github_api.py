import requests
import json
from datetime import datetime
import subprocess
from urllib3.exceptions import NewConnectionError, MaxRetryError


def get_merged_prs(repo, fields, n_max):
    fields_use = fields.replace("user", "author").replace("merged_at", "mergedAt").replace("merged_by", "mergedBy")
    output = subprocess.check_output(f"gh pr list --limit {n_max} --state merged --json {fields_use} --repo {repo}", shell=True)
    all_pr_data = json.loads(output)

    d = {d['number']: d for d in all_pr_data}

    for number in d.keys():
        d[number]['user'] = d[number]['author']
        d[number]['merged_at'] = d[number]['mergedAt']
        d[number]['merged_by'] = d[number]['mergedBy']
        d[number]['merge_time'] = datetime.strptime(d[number]['merged_at'], "%Y-%m-%dT%H:%M:%SZ")

    return d


def add_new_pr(repo, number, dict, fields):
    api_response = requests.get(
            f"https://api.github.com/repos/{repo}/pulls/{number}"
        )
    data = json.loads(api_response.text)
    dict[number] = {}
    for field in fields.split(","):
        dict[number][field] = data[field]

    dict[number]['merge_time'] = datetime.strptime(dict[number]['merged_at'], "%Y-%m-%dT%H:%M:%SZ")


def get_most_recent_updated_pr(repo, number_with_connection_error=1):
    try:
        url = f"https://github.com/{repo}/pulls?q=is%3Apr+is%3Aclosed+sort%3Aupdated-desc"
        r = requests.get(url, allow_redirects=True)
        lines = r.content.decode().split("\n")
        index = next((i for i in enumerate(lines) if "     #" in i[1]), [-1, -1])[0]
        return lines[index].split("#")[1]
    except requests.exceptions.ConnectionError or NewConnectionError or MaxRetryError:
        print("No connection")
        return number_with_connection_error
