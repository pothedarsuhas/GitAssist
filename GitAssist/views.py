from flask import request
from flask_restful import Resource, Api, reqparse
from github import *
import json

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
            repo = g.get_repo(owner+'/'+repo)
            branches = str(list(repo.get_branches())
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
                           '''
                           {
              "username" : "pothedarsuhas",
              "password" : "XXXXXXX",
              "working_branch" : "targetbranchname"
            }
                           '''
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
