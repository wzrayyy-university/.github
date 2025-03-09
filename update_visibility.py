import json
import os
import sys
import yaml
from datetime import datetime

import requests

def gh_exit(status: int, updated: bool = False):
    with open(os.environ['GITHUB_OUTPUT'], 'w') as f:
        f.write(f'updated={int(updated)}')
    exit(status)

if len(sys.argv) < 2:
    print("Missing token!", file=sys.stderr)
    gh_exit(1)

with open('metadata.json') as f:
    metadata = json.load(f)
    current_sem = metadata['last_available'] + 1

with open('index.yml') as f:
    data = yaml.safe_load(f)

if current_sem not in data['availability']:
    print('Availability date missing!')
    gh_exit(0)

if datetime.now() < datetime.strptime(data['availability'][current_sem], "%m/%d/%Y"):
    print("Nothing to do!")
    gh_exit(0)

HEADERS = {'Authorization': f'Bearer {sys.argv[1]}'}

status = False
for entry_name in data['assignments']:
    entry = data['assignments'][entry_name]

    projects = entry['projects'].get(current_sem) or []

    if not projects:
        continue

    print(f"Processing {entry['name']}")

    for project in projects:
        repo_prefix = f'wzrayyy-university/{entry_name}-'

        if type(project) is str:
            name = project
            repo = repo_prefix + project.lower().replace(' ', '-')
        else:
            name = project['name']
            repo = repo_prefix + project['repo']

        print(name + ': ', end='')
        sys.stdout.flush()
        r = requests.patch('https://api.github.com/repos/' + repo, json={'private': False}, headers=HEADERS)
        print('✅' if r.status_code == 200 else f'❌ {r.status_code} {r.json()["message"]}')
        status = r.status_code != 200 or status
    print()

# TODO: uncomment this
if status:
    gh_exit(status)

with open('metadata.json', 'w') as f:
    metadata['last_available'] += 1
    json.dump(metadata, f)

gh_exit(0, True)
