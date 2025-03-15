from collections.abc import Callable
import json
import os
import sys
import yaml
from datetime import datetime

import requests
from utils import *

PRIVATE = '\033[38;5;1mPRIVATE\033[0m'
PUBLIC = '\033[38;5;2mPUBLIC\033[0m'

metadata_changed = False

def gh_exit(status: int):
    if status == 0:
        with open(os.environ['GITHUB_OUTPUT'], 'w') as f:
            f.write(f'updated={int(metadata_changed)}')

        with open('metadata.json', 'w') as f:
            json.dump(metadata, f)
    exit(status)

if len(sys.argv) < 2:
    print("Missing token!", file=sys.stderr)
    gh_exit(1)


with open('index.yml') as f:
    data = yaml.safe_load(f)

with open('metadata.json') as f:
    metadata = json.load(f)
    next_sem_date = data['availability'].get(metadata['last_available'] + 1)
    if next_sem_date and datetime.now() > datetime.strptime(next_sem_date, "%m/%d/%Y"):
        metadata['last_available'] += 1
        metadata_changed = True
    current_sem = metadata['last_available']

HEADERS = {'Authorization': f'Bearer {sys.argv[1]}'}


def get_alignment(projects: dict[str, list], links: list) -> int:
    out = 0

    for project_semester in projects:
        for project in projects[project_semester]:
            out = max(len(get_project_info(project, '')[0]), out)

    for link in links:
        out = max(len(get_link_info(link, '')[0]), out)

    return out + 1


def make_request(repo: str, private: bool) -> tuple[int, str]:
    r = requests.patch('https://api.github.com/repos/' + repo, json={'private': private}, headers=HEADERS)
    return r.status_code, r.text


def process_entry[T](entry: T, private: Callable[[T], bool], get_info: Callable[[T], tuple[str, str]], alignment: int) -> bool:
    is_private = private(entry)
    name, repo = get_info(entry)

    # idc, this will come to bite me later
    if data['meta']['repo'] not in repo:
        return False

    alignment -= len(name)

    print(name + ':' + ' ' * alignment, end='')
    sys.stdout.flush()
    status, text = make_request(repo, is_private)

    if status != 200:
        print('ERROR', text)
    else:
        print(PRIVATE if is_private else PUBLIC)

    return status != 200


def main():
    status = False

    for entry_name in data['assignments']:
        repo_prefix = f"{data['meta']['repo']}/{entry_name}-"
        entry = data['assignments'][entry_name]
        projects: dict[str, list] = entry.get('projects') or {}
        links: list = entry.get('links') or []

        print(f"\033[1m--- {entry['name']} ---\033[0m")
        alignment = get_alignment(projects, links)

        for project_semester in projects:
            is_private = project_semester > current_sem
            for project in projects[project_semester]:
                status = process_entry(
                    project,
                    lambda _: is_private,
                    lambda p: get_project_info(p, repo_prefix)[:2],
                    alignment
                ) or status

        for link in links:
            status = process_entry(
                link,
                lambda l: l['visibility'] >= current_sem if 'visibility' in l else False,
                lambda l: get_link_info(l, repo_prefix),
                alignment
            ) or status
        print()

    gh_exit(status)

main()
