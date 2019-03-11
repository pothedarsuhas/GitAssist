from github import *
# import os
# import git
# from flask import Flask
# import glob, hashlib

# First create a Github instance:

# using username and password
g = Github("pothedarsuhas","XXXXXXXXXXX")

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

# repoName = "Jenkins" #repo
# repo = g.get_user().get_repo(repoName)
# WORKING_BRANCH = "MarioPuzo"
# base = repo.get_branch("master")
# head = repo.get_branch(WORKING_BRANCH)
# merge_to_master = repo.merge("master", head.commit.sha, "merge to master")

# sha = hashlib.sha1().hexdigest()

# repoName = 'Jenkins'
# repo = g.get_user().get_repo(repoName)

# Step 2: Prepare files to upload to GitHub
# files = glob.glob("C:/Users/1338826/PycharmProjects/IC2/Data-Structures-Algorithms/**", )
# print(files)
# # Step 3: Make a commit and push
# commit_message = 'Uploading files into ' + repoName
#
# tree = repo.get_git_tree(sha)
# repo.create_git_commit(commit_message, tree, [])
# repo.push()
#
# repo = Repo(repoName)
# commit_message = 'Add simple regression analysis'
# repo.index.add(files)
# repo.index.commit(commit_message)
# origin = repo.remote('origin')
# origin.push()

# import fnmatch
# import os
#
# matches = []
# for root, dirnames, filenames in os.walk('C:/Users/1338826/PycharmProjects/IC2/Data-Structures-Algorithms'):
#     for filename in fnmatch.filter(filenames, '*'):
#         matches.append(os.path.join(root, filename).replace('\\','/'))
#
# print(matches)
#
# repoName = 'Jenkins'
# repo = Repo(repoName)
# commit_message = 'new things getting added'
# repo.index.add(matches)
# repo.index.commit(commit_message)
# origin = repo.remote('origin')
# origin.push()



import os, fnmatch, base64
from github import Github
from github import InputGitTreeElement

user = "pothedarsuhas"
password = "XXXXXXXXX"
repo = 'Jenkins'
branch = 'master'
path = "C:/Users/1338826/PycharmProjects/IC2/Data-Structures-Algorithms"
# g = Github(user,password)
# repo = g.get_user().get_repo(repo)
matches = []
for root, dirnames, filenames in os.walk(path):
    for filename in fnmatch.filter(filenames, '*'):
        matches.append(os.path.join(root, filename).replace('\\','/'))

print(matches)

# commit_message = 'python update 2'
#
# branch_ref = repo.get_git_ref('heads/' + branch)
# branch_sha = branch_ref.object.sha
# base_tree = repo.get_git_tree(branch_sha)
# element_list = list()
# for i, entry in enumerate(matches):
#     with open(entry) as input_file:
#         data = input_file.read()
#     element = InputGitTreeElement(matches[i], '100644', 'blob', data)
#     element_list.append(element)
# tree = repo.create_git_tree(element_list, base_tree)
# parent = repo.get_git_commit(branch_sha)
# commit = repo.create_git_commit(commit_message, tree, [parent])
# branch_ref.edit(commit.sha)

import github3

gh = github3.login('pothedarsuhas', 'Suhaspb@19')
repository = gh.repository('pothedarsuhas', 'Jenkins')
sha = repository.create_blob('Testing blob creation', 'utf-8')
print(sha)
for file_info in matches:
    with open(file_info, 'rb') as fd:
        contents = fd.read()
    # repository.create_file(
    #     path=file_info,
    #     message='Start tracking {!r}'.format(file_info),
    #     content=contents,
    #     branch = 'lex'
    # )
r = gh.repository('pothedarsuhas','OpenshiftRepo')
r.delete()


