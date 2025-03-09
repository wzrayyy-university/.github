import yaml

with open('index.yml') as f:
    data = yaml.safe_load(f)

output = ''

output += f"# {data['meta']['name']}\n"
if 'note' in data['meta']:
    output += f"> [!NOTE]\n> {data['meta']['note']}\n"

for entry_name in sorted(data['assignments']):
    repo_prefix = f'https://github.com/wzrayyy-university/{entry_name}-'

    entry = data['assignments'][entry_name]
    projects = entry['projects']

    output += f"## {entry['name']}\n"
    numbered = bool(entry.get('numbered') != False)

    if 'description' in entry:
        output += f"{entry['description']}  \n\n"

    if 'links' in entry:
        links = entry['links']
        if type(links) is list:
            output += ', '.join([f"[{link['name']}]({link['url']})" for link in links])
        else:
            output += entry['links']
        output += '\n'

    show_semester = len(projects) > 1 and sum([len(projects[i]) for i in projects]) > len(projects)
    idx = 1

    for project_semester in projects:
        output += f'### Semester {project_semester}\n' if show_semester else ''
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
