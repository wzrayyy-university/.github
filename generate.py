import yaml

with open('index.yml') as f:
    data = yaml.safe_load(f)

output = """
# University index

> [!NOTE]
> All repositories will remain private until the end of the exam session.

"""

for entry_name in data:
    repo_prefix = f'https://github.com/wzrayyy-university/{entry_name}-'

    entry = data[entry_name]
    projects = (entry.get('projects') or []) + (entry.get('hidden') or [])

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
    for project in projects:
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
