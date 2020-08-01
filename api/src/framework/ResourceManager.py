import flask
import flask_restful
from python_helper import Constant
import Security, FlaskManager, Serializer
from MethodWrapper import Method

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
        app = flask.Flask(rootName)
        api = flask_restful.Api(app)
        jwt = Security.getJwtMannager(app, jwtSecret)

        FlaskManager.addGlobalsTo(api)
        args = [api, app, jwt]
        for kwResource in FlaskManager.KW_RESOURCE_LIST :
            args.append(getResourceList(api,kwResource))
        args.append(refferenceModel)
        FlaskManager.addFlaskApiResources(*args, databaseEnvironmentVariable=databaseEnvironmentVariable, localStorageName=localStorageName)

        return api, app, jwt
