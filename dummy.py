from github import *
import os
# import git
from flask import Flask
import glob, hashlib


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

# repoName = "Jenkins" #repo
# repo = g.get_user().get_repo(repoName)
# WORKING_BRANCH = "MarioPuzo"
# base = repo.get_branch("master")
# head = repo.get_branch(WORKING_BRANCH)
# merge_to_master = repo.merge("master", head.commit.sha, "merge to master")


from github import *
from git import Repo
# import subprocess

# First create a Github instance:

# using username and password
# g = Github("pothedarsuhas","XXXXXXXXXXXXx")

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

# owner = "pothedarsuhas"
# repository = "Jenkins"
# git_url = "https://github.com/"+owner+'/'+repository+'.git'   # https://github.com/pothedarsuhas/Jenkins.git
# repo_dir = "/Users/suhaspothedar/Downloads/"+repository
# branch = 'master'
# Repo.clone_from(git_url, repo_dir,branch= branch)

# import fnmatch # getting all files in directory
# import os

# matches = []
# for root, dirnames, filenames in os.walk('C:/Users/1338826/PycharmProjects/IC2/Data-Structures-Algorithms'):
#     for filename in fnmatch.filter(filenames, '*'):
#         matches.append(os.path.join(root, filename).replace('\\','/'))

# print(matches)

# repoName = 'Jenkins'
# repo = Repo(repoName)
# commit_message = 'new things getting added'
# repo.index.add(matches)
# repo.index.commit(commit_message)
# origin = repo.remote('origin')
# origin.push()
