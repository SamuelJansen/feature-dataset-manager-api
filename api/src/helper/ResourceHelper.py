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
def getResourceList(apiInstance,resourceType) :
    resourceNameList = getResourceNameList(
        apiInstance.globals.apiTree[apiInstance.globals.apiPackage],
        resourceType
    )
    resourceList = []
    for resourceName in resourceNameList :
        importedResourceList = Serializer.importResourceList(resourceName)
        if importedResourceList :
            for resource in importedResourceList :
                if resource :
                    resourceList.append(resource)
    return resourceList

@Method
def initializeResources(api, refferenceModel, localStorageName = None) :
    FlaskHelper.addGlobalsTo(api)
    FlaskHelper.addFlaskApiResources(
        api,
        getResourceList(api,FlaskHelper.KW_CONTROLLER_RESOURCE),
        getResourceList(api,FlaskHelper.KW_SERVICE_RESOURCE),
        getResourceList(api,FlaskHelper.KW_REPOSITORY_RESOURCE),
        getResourceList(api,FlaskHelper.KW_HELPER_RESOURCE),
        getResourceList(api,FlaskHelper.KW_CONVERTER_RESOURCE),
        refferenceModel,
        localStorageName = localStorageName
    )
