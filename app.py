from flask import Flask
from GitAssist.views import *


app = Flask(__name__, instance_relative_config = True)
api = Api(app)

# Load the default configuration
app.config.from_object('config')

# Load the configuration from the instance folder
app.config.from_pyfile('config.py')

# for free users
api.add_resource(user_repo, '/user/repos') #ceates a repository
api.add_resource(repos_owner_repo, '/repos/<string:owner>/<string:repo>') #deletes a repository
api.add_resource(repos_owner_repo_branches, '/repos/<string:owner>/<string:repo>/branches') #lists the branches in a repository


#for organizations

if __name__ == '__main__':
    app.run( debug = app.config["DEBUG"])