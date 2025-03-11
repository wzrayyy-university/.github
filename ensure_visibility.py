import json
import os
import sys
import yaml
from datetime import datetime

import requests

metadata_changed = False

def gh_exit(status: int):
    with open(os.environ['GITHUB_OUTPUT'], 'w') as f:
        f.write(f'updated={int(metadata_changed)}')
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
        with open('metadata.json', 'w') as f:
            json.dump(metadata, f)
        metadata_changed = True
    current_sem = metadata['last_available']

HEADERS = {'Authorization': f'Bearer {sys.argv[1]}'}

status = False

for entry_name in data['assignments']:
    entry = data['assignments'][entry_name]

    projects = entry['projects']

    if not projects:
        continue

    print(f"Processing {entry['name']}")

    for project_semester in projects:
        is_private = project_semester > current_sem

        for project in projects[project_semester]:
            repo_prefix = f'wzrayyy-university/{entry_name}-'

            if type(project) is str:
                name = project
                repo = repo_prefix + project.lower().replace(' ', '-')
            else:
                name = project['name']
                repo = repo_prefix + project['repo']

            print(name + ': ', end='')
            sys.stdout.flush()
            r = requests.patch('https://api.github.com/repos/' + repo, json={'private': is_private}, headers=HEADERS)

            if r.status_code != 200:
                print('Error!')
                print(r.text)
            else:
                print('PRIVATE' if is_private else 'PUBLIC')
            status = r.status_code != 200 or status
    print()

gh_exit(status)
