import github3
from flask import request
from flask_restful import Resource, reqparse, Api
from github import *
import os, fnmatch
import logging
# from git import *
from models import Log

logging.basicConfig(format='%(asctime)s\t[%(levelname)s]\t%(message)s', filename = "C:\\Users\\1338826\\PycharmProjects\\IC2\\GitAssist\\Logs\\GitAssist.log")
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


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
        logger.info("Data validation from request body complete")
        data = request.get_json()
        logger.info("Data fetch from the request body complete")
        username = data['username']
        password = data['password']

        try:
            g = Github(username, password)

            repositories = []
            for repo in g.get_user().get_repos():
                repositories.append(repo.name)
            logger.info("Successfully Authenticated")
            logger.info("Repository list is returned")
            log = Log(username = username, operation = "List Repository", operation_status = 0)
            log.save()
            return {"repository list": repositories}, 200
        except GithubException as e:
            response_code = str(e) #gihub eception object is not subscriptable
            logger.error("Request body format or the values passed are not valid")
            log = Log(username=username, operation="List Repository", operation_status = 1)
            log.save()
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
        logger.info("Data validation from request body complete")
        data = request.get_json()
        logger.info("Data fetch from the request body complete")

        username = data['username']
        password = data['password']
        # authorization = data['authorization']
        name = data['name']
        description = data['description']

        try:
            g = Github(username, password)
            logger.info("Successfully Authenticated")
            user = g.get_user()
            user.create_repo(name, description)
            logger.info("Repository is created")
            logger.error("Request body format or the values passed are not valid")
            return {"repository name": name, "creation_status": "success"}, 201

        except GithubException as e:
            response_code = str(e) #gihub eception object is not subscriptable
            logger.error("Request body format or the values passed are not valid")
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
        logger.info("Data validation from request body complete")
        data = request.get_json()
        logger.info("Data fetch from the request body complete")
        username = data['username']
        password = data['password']
        name = data['name']
        try:
            g = Github(username, password)
            repository = g.get_repo(owner+'/'+repo)
            logger.info("Successfully Authenticated")
            repository.delete()
            logger.info("Repository is deleted")
            return {"repository name": repo, "deletion_status": "success"}, 200

        except GithubException as e:
            response_code = str(e) #gihub eception object is not subscriptable
            logger.error("Request body format or the values passed are not valid")
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
        logger.info("Data validation from request body complete")

        data = request.get_json()
        logger.info("Data fetch from the request body complete")
        username = data['username']
        password = data['password']

        try:
            g = Github(username, password)
            repo = g.get_repo(owner+'/'+repo)
            branches = str(list(repo.get_branches()))
            logger.info("Successfully Authenticated")
            logger.info("Branches list is returned")
            return {"branches": branches}, 200

        except GithubException as e:
            response_code = str(e) #gihub eception object is not subscriptable
            logger.error("Request body format or the values passed are not valid")
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
        logger.info("Data validation from request body complete")
        data = request.get_json()
        logger.info("Data fetch from the request body complete")
        username = data['username']
        password = data['password']
        target_branch = data['ref']
        source_branch = "master"

        try:
            g = Github(username, password)
            repo = g.get_user().get_repo(repo)
            sb = repo.get_branch(source_branch)
            repo.create_git_ref('refs/heads/' + target_branch, sb.commit.sha)
            logger.info("Successfully Authenticated")
            logger.info("Branch is created")
            return {"branch": target_branch, "creation_status": "success"}, 201

        except GithubException as e:
            response_code = str(e) #gihub eception object is not subscriptable
            logger.error("Request body format or the values passed are not valid")
            return {"branch name": target_branch, "creation_status": "failure", "exception" : str(e)}, response_code[:3]

class repos_owner_repo_merges(Resource):

    def post(self, owner, repo):
        parser = reqparse.RequestParser()
        parser.add_argument("username", required=True)
        parser.add_argument("password", required=True)
        parser.add_argument("working_branch", required = True)
        logger.info("Data validation from request body complete")
        data = request.get_json()
        logger.info("Data fetch from the request body complete")
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
            logger.info("Successfully Authenticated")
            logger.info("Branch is merged")
            return {"branch": working_branch, "merge_status": "success"}, 201

        except GithubException as e:
            response_code = str(e) #gihub eception object is not subscriptable
            logger.error("Request body format or the values passed are not valid")
            return {"branch": working_branch, "merge_status": "failure", "exception" : str(e)}, response_code[:3]

# class repos_owner_repo_clones(Resource):
#
#     def post(self, owner, repo):
#         '''
#                            {
#               "branch" : "targetbranchname"
#             }
#         '''
#         parser = reqparse.RequestParser()
#         parser.add_argument("branch", required=True)
#         logger.info("Data validation from request body complete")
#         branch = 'master'
#         data = request.get_json()
#         logger.info("Data fetch from the request body complete")
#         if 'branch' not in data.keys():
#             pass
#         else:
#             branch = data['branch']
#         try:
#             repository = repo
#             git_url = "https://github.com/" + owner + '/' + repository + '.git'  # https://github.com/pothedarsuhas/Jenkins.git
#             repo_dir = "/Users/suhaspothedar/Downloads/" + repository + '-' + branch #hardcoded currently for ease of development
#             Repo.clone_from(git_url, repo_dir, branch=branch)
#             logger.info("Successfully Authenticated")
#             logger.info("Repository's specified branch cloned successfully")
#             return {"repository": repo, "branch": branch, "clone_status": "success"}, 200
#         except GithubException  as e:
#             response_code = str(e) #gihub eception object is not subscriptable
#             logger.error("Request body format or the values passed are not valid")
#             return {"repository": repo, "branch": branch, "clone_status": "failure", "exception" : str(e)}, response_code[:3]
#         except GitError  as e:
#             logger.error("Request body format or the values passed are not valid")
#             return {"repository": repo, "branch": branch, "clone_status": "failure", "exception" : str(e)}, 404

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
        logger.info("Data validation from request body complete")
        data = request.get_json()
        logger.info("Data fetch from the request body complete")

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
            # print(matches)
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
            logger.info("Successfully Authenticated")
            logger.info("Uploaded to a Repository's specific branch")
            return {"branch name": branch, "upload_status": "success"}, 201

        except github3.GitHubError as e:
            response_code = str(e) #gihub3 eception object is not subscriptable
            logger.error("Request body format or the values passed are not valid")
            return {"branch name": branch, "upload_status": "failure", "exception" : str(e)}, response_code[:3]





