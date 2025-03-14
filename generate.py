import yaml
from utils import *

with open('index.yml') as f:
    data = yaml.safe_load(f)

output = f"# {data['meta']['name']}\n"

if 'note' in data['meta']:
    output += f"> [!NOTE]\n> {data['meta']['note']}\n"

if 'highlights' in data:
    highlights = data['highlights']
    output += '## Highlights\n'

    for work in highlights:
        output += f"* **[{work['name']}](https://github.com/wzrayyy-university/{work['repo']})**  \n"
        if 'description' in work:
            output += f"    **{work['description']}**\n"

for entry_name in data['assignments']:
    repo_prefix = f"https://github.com/{data['meta']['repo']}/{entry_name}-"
    entry = data['assignments'][entry_name]
    projects: dict = entry.get('projects') or {}
    links: list = entry.get('links') or []

    output += f"## {entry['name']}\n"
    numbered = entry.get('numbered') != False

    if 'description' in entry:
        output += f"{entry['description']}  \n\n"

    if links:
        links_printable = []
        for link in links:
            name, url = get_link_info(link, repo_prefix)
            links_printable.append(f"[{name}]({url})")
        output += ', '.join(links_printable) + '\n'

    if 'show_semesters' in entry:
        show_semesters = entry['show_semesters']
    else:
        show_semesters = len(projects) > 1 and sum([len(projects[i]) for i in projects]) > len(projects)

    idx = 1
    for project_semester in projects:
        output += f'### Semester {project_semester}\n' if show_semesters else ''
        for project in projects[project_semester]:
            name, repo, project_idx = get_project_info(project, repo_prefix)

            idx = idx if project_idx == -1 else project_idx

            if numbered:
                output += f'{idx}. [{name}]({repo})\n'
                idx += 1
            else:
                output += f'* [{name}]({repo})\n'

with open("profile/README.md", 'w') as f:
    f.write(output.strip() + '\n')
