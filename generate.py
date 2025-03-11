import yaml

with open('index.yml') as f:
    data = yaml.safe_load(f)

with open('metadata.json') as f:
    current_semester = yaml.safe_load(f)['last_available'] + 1

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

for entry_name in sorted(data['assignments']):
    repo_prefix = f'https://github.com/wzrayyy-university/{entry_name}-'

    entry = data['assignments'][entry_name]
    projects = entry['projects']

    output += f"## {entry['name']}\n"
    numbered = bool(entry.get('numbered') != False)

    if 'description' in entry:
        output += f"{entry['description']}  \n\n"

    if 'links' in entry:
        links = []
        for link in entry['links']:
            if type(link) is str:
                name = link
                url = repo_prefix + link.lower().replace(' ', '-')
            else:
                if 'visibility' in link and link['visibility'] >= current_semester:
                    continue

                name = link['name']
                if 'repo' in link:
                    url = repo_prefix + link['repo']
                else:
                    url = link['url']
            links.append(f"[{name}]({url})")
        output += ', '.join(links)
        output += '\n'

    if 'show_semesters' in entry:
        show_semesters = entry['show_semesters']
    else:
        show_semesters = len(projects) > 1 and sum([len(projects[i]) for i in projects]) > len(projects)
    idx = 1

    for project_semester in projects:
        output += f'### Semester {project_semester}\n' if show_semesters else ''
        for project in projects[project_semester]:
            if type(project) is str:
                name = project
                repo = repo_prefix + project.lower().replace(' ', '-')
            else:
                name = project['name']
                repo = repo_prefix + project['repo']
                if 'idx' in project:
                    idx = project.get('idx')

            if numbered:
                output += f'{idx}. [{name}]({repo})\n'
                idx += 1
            else:
                output += f'* [{name}]({repo})\n'

with open("profile/README.md", 'w') as f:
    f.write(output.strip() + '\n')
