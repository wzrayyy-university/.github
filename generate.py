import yaml

with open('index.yml') as f:
    data = yaml.safe_load(f)

output = """
# University index

> [!NOTE]
> All repositories will remain private until the end of the exam session.

"""

for entry_name in data['repos']:
    repo_prefix = f'https://github.com/wzrayyy-university/{entry_name}-'

    entry = data['repos'][entry_name]
    projects = entry['projects']

    output += f"## {entry['name']}\n"
    numbered = bool(entry.get('numbered') != False)

    if 'extras' in entry:
        output += '\n'
        extras = entry['extras']
        if type(extras) is list:
            output += '\n'.join(extras)
            output += '\n\n'
        else:
            output += entry['extras'] + '\n\n'

    idx = 1

    show_semester = len(projects) > 1 and sum([len(projects[i]) for i in projects]) > len(projects)

    for project_semester in projects:
        output += f'\n#### Semester {project_semester}\n' if show_semester else ''
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
    output += '\n'


with open("profile/README.md", 'w') as f:
    f.write(output.strip() + '\n')
