from flask import Flask
from flask_restful import Api
from python_helper import Constant
from MethodWrapper import Method
import Security, FlaskManager, Serializer

DOT_PY = '.py'

@Method
def getResourceName(resourceFileName) :
    return resourceFileName.split(DOT_PY)[0]

@Method
def isResourceType(resourceFileName,resourceType) :
    splitedResourceFileName = resourceFileName.split(resourceType)
    return len(splitedResourceFileName)>1 and splitedResourceFileName[1] == DOT_PY

@Method
def getResourceNameList(apiTree, resourceType) :
    resourceNameList = []
    if apiTree or type(apiTree).__name__ == Constant.DICT :
        for package,subPackageTree in apiTree.items() :
            if isResourceType(package,resourceType) :
                resourceNameList.append(getResourceName(package))
            resourceNameList += getResourceNameList(
                subPackageTree,
                resourceType
            )
    return resourceNameList

@Method
def getControllerNameList(controllerName) :
    controllerNameList = [controllerName]
    controllerNameList.append(f'{controllerName[:-len(FlaskManager.KW_CONTROLLER_RESOURCE)]}{Serializer.KW_BATCH}{FlaskManager.KW_CONTROLLER_RESOURCE}')
    # controllerNameList = [name for name in dir(__import__(controllerName)) if not name.startswith(Constant.UNDERSCORE)]
    # return Serializer.getAttributeNameList(__import__(controllerName))
    return controllerNameList

@Method
def getControllerList(resourceName):
    controllerNameList = getControllerNameList(resourceName)
    importedControllerList = []
    for controllerName in controllerNameList :
        resource = Serializer.importResource(controllerName, resourceModuleName=resourceName)
        if resource :
            importedControllerList.append(resource)
    return importedControllerList

@Method
def getResourceList(apiInstance, resourceType) :
    resourceNameList = getResourceNameList(
        apiInstance.globals.apiTree[apiInstance.globals.apiPackage],
        resourceType
    )
    resourceList = []
    for resourceName in resourceNameList :
        if FlaskManager.KW_CONTROLLER_RESOURCE == resourceName[-len(FlaskManager.KW_CONTROLLER_RESOURCE):] :
            resourceList += getControllerList(resourceName)
        else :
            resource = Serializer.importResource(resourceName)
            if resource :
                resourceList.append(resource)
    return resourceList

@Method
def initialize(
        rootName,
        refferenceModel,
        databaseEnvironmentVariable  = None,
        localStorageName = None,
        jwtSecret = None
    ) :

        # # bluePrint = Blueprint('feature-manager', __name__, url_prefix='/api/')
        # # api = Api(version='1.0', title='Feature dataset manager', description='A feature manager api')
        # # ns = api.namespace('test', description='Just a test')
        # # app = Flask(rootName)
        # # app.register_blueprint(api)
        #
        # from werkzeug.contrib.fixers import ProxyFix
        # app = Flask(rootName)
        # # app.wsgi_app = ProxyFix(app.wsgi_app)
        # api = Api(app, version='1.0', title='Feature dataset manager', description='A feature manager api')
        # # ns = api.namespace('test', description='Just a test')
        #
        # # from flask import Blueprint
        # # from flask_restplus import Namespace
        # #
        # # blueprint = Blueprint('api', rootName, url_prefix='/api')
        # # api = Api(blueprint)
        # # global_namespace = Namespace('global', path='/global')
        # # api.add_namespace(global_namespace)
        # # app = Flask(__name__)
        # # app.register_blueprint(blueprint, url_prefix='')

        globalNamespace = ''
        app = Flask(rootName)
        api = Api(app)
        jwt = Security.getJwtMannager(app, jwtSecret)

        FlaskManager.addGlobalsTo(api)
        args = [api, app, globalNamespace, jwt]
        for kwResource in FlaskManager.KW_RESOURCE_LIST :
            args.append(getResourceList(api,kwResource))
        args.append(refferenceModel)
        FlaskManager.addFlaskApiResources(*args, databaseEnvironmentVariable=databaseEnvironmentVariable, localStorageName=localStorageName)

        return api, app, jwt
