import github3
from flask import request
from flask_restful import Resource, Api, reqparse
from github import *
import os, fnmatch
from github3 import login, repository

class user_repo(Resource):

    def get(self):
        '''
            list repositories
            sample request
            {
              "username" : "pothedarsuhas",
              "password" : "XXXXXXXXXX"
            }
            '''
        parser = reqparse.RequestParser()
        parser.add_argument("username", required=True)
        parser.add_argument("password", required=True)

        data = request.get_json()

        username = data['username']
        password = data['password']

        try:
            g = Github(username, password)
            repositories = []
            for repo in g.get_user().get_repos():
                repositories.append(repo.name)
            return {"repository list": repositories}, 200
        except GithubException as e:
            response_code = str(e) #gihub eception object is not subscriptable
            return {"message": "cant fetch repositories", "exception" : str(e)}, response_code[:3]

    def post(self):
        '''
            repository creation
            sample request
            {
              "name": "Hello-World",
              "description": "This is your first repository",
              "username" : "pothedarsuhas",
              "password" : "XXXXXXXXXX"
            }
            '''
        parser = reqparse.RequestParser()
        parser.add_argument("username", required = True)
        parser.add_argument("password", required = True)
        parser.add_argument("name", required = True)
        parser.add_argument("description", required = True)
        data = request.get_json()

        username = data['username']
        password = data['password']
        # authorization = data['authorization']
        name = data['name']
        description = data['description']

        try:
            g = Github(username, password)
            user = g.get_user()
            user.create_repo(name, description)
            return {"repository name": name, "creation_status": "success"}, 201

        except GithubException as e:
            response_code = str(e) #gihub eception object is not subscriptable
            return {"repository name": name, "creation_status": "failed", "exception" : str(e)}, response_code[:3]

class repos_owner_repo(Resource):

    def delete(self, owner, repo):
        '''
            repository deletion using path variables
        '''
        parser = reqparse.RequestParser()
        parser.add_argument("username", required=True)
        parser.add_argument("password", required=True)
        parser.add_argument("name", required=True)
        data = request.get_json()

        username = data['username']
        password = data['password']
        name = data['name']
        try:
            g = Github(username, password)
            repository = g.get_repo(owner+'/'+repo)
            repository.delete()
            return {"repository name": repo, "deletion_status": "success"}, 200

        except GithubException as e:
            response_code = str(e) #gihub eception object is not subscriptable
            return {"repository name": repo, "deletion_status": "failed", "exception" : str(e)}, response_code[:3]


class repos_owner_repo_branches(Resource):

    def get(self, owner, repo):
        '''
            list branches
            sample request
            {
              "username" : "pothedarsuhas",
              "password" : "XXXXXXXXXX"
            }
        '''
        parser = reqparse.RequestParser()
        parser.add_argument("username", required=True)
        parser.add_argument("password", required=True)

        data = request.get_json()

        username = data['username']
        password = data['password']

        try:
            g = Github(username, password)
            repo = g.get_repo(owner+'/'+repo)
            branches = str(list(repo.get_branches()))
            return {"branches": branches}, 200

        except GithubException as e:
            response_code = str(e) #gihub eception object is not subscriptable
            return {"message": "cant fetch branches", "exception" : str(e)}, response_code[:3]

class repos_owner_repo_git_refs(Resource):

    def post(self, owner, repo):
        '''
            create branches
            sample request
            {
              "username" : "pothedarsuhas",
              "password" : "XXXXXXXXXX",
              "ref" : "targetbranchname"
            }
        '''
        parser = reqparse.RequestParser()
        parser.add_argument("username", required=True)
        parser.add_argument("password", required=True)
        parser.add_argument("ref", required=True)
        data = request.get_json()

        username = data['username']
        password = data['password']
        target_branch = data['ref']
        source_branch = "master"

        try:
            g = Github(username, password)
            repo = g.get_user().get_repo(repo)
            sb = repo.get_branch(source_branch)
            repo.create_git_ref('refs/heads/' + target_branch, sb.commit.sha)
            return {"branch": target_branch, "creation_status": "success"}, 201

        except GithubException as e:
            response_code = str(e) #gihub eception object is not subscriptable
            return {"branch name": target_branch, "creation_status": "failure", "exception" : str(e)}, response_code[:3]

class repos_owner_repo_merges(Resource):

    def post(self, owner, repo):
        parser = reqparse.RequestParser()
        parser.add_argument("username", required=True)
        parser.add_argument("password", required=True)
        parser.add_argument("working_branch", required = True)
        data = request.get_json()

        username = data['username']
        password = data['password']
        working_branch = data['working_branch']
        source_branch = "master"

        try:
            g = Github(username, password)
            repoName = repo  # repo
            repo = g.get_user().get_repo(repoName)
            WORKING_BRANCH = working_branch
            base = repo.get_branch(source_branch)
            head = repo.get_branch(WORKING_BRANCH)
            repo.merge("master", head.commit.sha, "merge to master")
            return {"branch": working_branch, "merge_status": "success"}, 201

        except GithubException as e:
            response_code = str(e) #gihub eception object is not subscriptable
            return {"branch": working_branch, "merge_status": "failure", "exception" : str(e)}, response_code[:3]

class repos_owner_repo_clones(Resource):

    def post(self, owner, repo):
        '''
                           {
              "branch" : "targetbranchname"
            }
        '''
        parser = reqparse.RequestParser()
        parser.add_argument("branch", required=True)
        branch = 'master'
        data = request.get_json()
        if 'branch' not in data.keys():
            pass
        else:
            branch = data['branch']
        try:
            repository = repo
            git_url = "https://github.com/" + owner + '/' + repository + '.git'  # https://github.com/pothedarsuhas/Jenkins.git
            repo_dir = "/Users/suhaspothedar/Downloads/" + repository + '-' + branch #hardcoded currently for ease of development
            Repo.clone_from(git_url, repo_dir, branch=branch)
            return {"repository": repo, "branch": branch, "clone_status": "success"}, 200
        except GithubException  as e:
            response_code = str(e) #gihub eception object is not subscriptable
            return {"repository": repo, "branch": branch, "clone_status": "failure", "exception" : str(e)}, response_code[:3]
        except GitError  as e:
            return {"repository": repo, "branch": branch, "clone_status": "failure", "exception" : str(e)}, 404

class repos_owner_repo_contents(Resource):

    def post(self, owner, repo):
        '''
            upload to specific branch
            {
        	"user" : "pothedarsuhas",
        	"password" : "Suhaspb@19",
            "branch" : "newbranch",
            "path" : "C:/Users/1338826/PycharmProjects/IC2/Data-Structures-Algorithms"
            }
            '''
        parser = reqparse.RequestParser()
        parser.add_argument("username", required=True)
        parser.add_argument("password", required=True)
        parser.add_argument("ref", required=True)
        data = request.get_json()

        username = data['username']
        password = data['password']
        branch = data['branch']
        path =  data['path']

        try:
            gh = github3.login(username, password)
            matches = []
            for root, dirnames, filenames in os.walk(path):
                for filename in fnmatch.filter(filenames, '*'):
                    matches.append(os.path.join(root, filename).replace('\\', '/'))
            print(matches)
            repository = gh.repository('pothedarsuhas', 'Jenkins')
            for file_info in matches:
                with open(file_info, 'rb') as fd:
                    contents = fd.read()
                repository.create_file(
                    path=file_info,
                    message='Start tracking {!r}'.format(file_info),
                    content=contents,
                    branch= branch
                )
            return {"branch name": branch, "upload_status": "success"}, 201

        except github3.GitHubError as e:
            response_code = str(e) #gihub3 eception object is not subscriptable
            return {"branch name": branch, "upload_status": "failure", "exception" : str(e)}, response_code[:3]





