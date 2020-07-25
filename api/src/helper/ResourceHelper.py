from python_helper import Constant
import FlaskHelper, Serializer
from MethodWrapper import Method

@Method
def getResourceName(resourceFileName) :
    return resourceFileName.split('.py')[0]

@Method
def isResourceType(resourceFileName,resourceType) :
    splitedResourceFileName = resourceFileName.split(resourceType)
    return len(splitedResourceFileName)>1 and splitedResourceFileName[1] == '.py'

@Method
def getResourceNameList(apiTree,resourceType) :
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
    # return getAttributeNameList(__import__(resourceFileName))
    controllerNameList = [controllerName]
    controllerNameList.append(f'{controllerName[:-len(FlaskHelper.KW_CONTROLLER_RESOURCE)]}Batch{FlaskHelper.KW_CONTROLLER_RESOURCE}')
    return controllerNameList

@Method
def getControllerList(resourceName):
    controllerNameList = getControllerNameList(resourceName)
    importedControllerList = []
    for controllerName in controllerNameList :
        resource = Serializer.importResource(controllerName, resourceFileName = resourceName)
        if resource :
            importedControllerList.append(resource)
    return importedControllerList

@Method
def getResourceList(apiInstance,resourceType) :
    resourceNameList = getResourceNameList(
        apiInstance.globals.apiTree[apiInstance.globals.apiPackage],
        resourceType
    )
    resourceList = []
    for resourceName in resourceNameList :
        if FlaskHelper.KW_CONTROLLER_RESOURCE == resourceName[-len(FlaskHelper.KW_CONTROLLER_RESOURCE):] :
            resourceList += getControllerList(resourceName)
        else :
            resource = Serializer.importResource(resourceName)
            if resource :
                resourceList.append(resource)
    return resourceList

@Method
def initializeResources(api, refferenceModel, localStorageName = None) :
    FlaskHelper.addGlobalsTo(api)
    args = [api]
    for kwResource in FlaskHelper.KW_RESOURCE_LIST :
        args.append(getResourceList(api,kwResource))
    args.append(refferenceModel)
    FlaskHelper.addFlaskApiResources(*args, localStorageName=localStorageName)
    # FlaskHelper.addFlaskApiResources(
    #     api,
    #     getResourceList(api,FlaskHelper.KW_CONTROLLER_RESOURCE),
    #     getResourceList(api,FlaskHelper.KW_SERVICE_RESOURCE),
    #     getResourceList(api,FlaskHelper.KW_REPOSITORY_RESOURCE),
    #     getResourceList(api,FlaskHelper.KW_VALIDATOR_RESOURCE),
    #     getResourceList(api,FlaskHelper.KW_HELPER_RESOURCE),
    #     getResourceList(api,FlaskHelper.KW_CONVERTER_RESOURCE),
    #     refferenceModel,
    #     localStorageName = localStorageName
    # )
