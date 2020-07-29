import flask
import flask_restful
import ResourceHelper
import ModelAssociation

app = flask.Flask(__name__)
api = flask_restful.Api(app)

ResourceHelper.initializeResources(
    api,
    app,
    ModelAssociation.Model,
    localStorageName = 'LocalFeatureManager'
)
