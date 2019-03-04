from github import *

# First create a Github instance:

# using username and password
g = Github("pothedarsuhas","XXXXXXXXXXXXx")

# or using an access token
# g = Github("XXXXXXXXXXXXXXXXXXXXX")

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


# repoName = "Jenkins" #repo
# source_branch = 'master'
# target_branch = 'newbranch' #ref
# repo = g.get_user().get_repo(repoName)
# sb = repo.get_branch(source_branch)
# repo.create_git_ref('refs/heads/' + target_branch, sb.commit.sha)
# print(repo.get_git_ref('heads/master'))
