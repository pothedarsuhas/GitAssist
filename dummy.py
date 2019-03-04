from github import *

# First create a Github instance:

# using username and password
g = ()

# or using an access token
g = Github("36f8c6524c23908337c55ccb400c7cbeb5bb74b6")

# Github Enterprise with custom hostname
# g = Github(base_url="https://{hostname}/api/v3", login_or_token="access_token")

# Then play with your Github objects:
# for repo in g.get_user().get_repos():
#     print(repo.name)

# repo = g.get_repo('pothedarsuhas/Python')
# contents = repo.get_contents("")
# for content_file in contents:
#     print(content_file)

# repo = g.get_repo("pothedarsuhas/GitAssist")
# a = str(list(repo.get_branches()))
# print(a)


repoName = "Jenkins"
source_branch = 'master'
target_branch = 'new branch'
repo = g.get_user().get_repo(repoName)
sb = repo.get_branch(source_branch)
repo.create_git_ref(ref=target_branch, sha=sb.commit.sha)