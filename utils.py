def get_project_info(project, repo_prefix: str) -> tuple[str, str, int]:
    if type(project) is str:
        return project, repo_prefix + project.lower().replace(' ', '-'), -1
    else:
        return project['name'], repo_prefix + project['repo'], project.get('idx') or -1


def get_link_info(link, repo_prefix: str) -> tuple[str, str]:
    if type(link) is str:
        return link, repo_prefix + link.lower().replace(' ', '-')
    else:
        if 'repo' in link:
            return link['name'], repo_prefix + link['repo']
        else:
            return link['name'], link['url']
