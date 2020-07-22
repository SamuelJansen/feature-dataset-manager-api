import webbrowser
from python_helper import log, Constant
import flask_restful
from flask_restful import reqparse, abort
from flask import Response, request
from MethodWrapper import Method
import Serializer, SqlAlchemyHelper

KW_URL = 'url'
KW_DEFAULT_URL = 'defaultUrl'
KW_MODEL = 'model'
KW_API = 'api'

KW_METHOD = 'method'

KW_RESOURCE = 'resource'

KW_CONTROLLER_RESOURCE = 'Controller'
KW_SERVICE_RESOURCE = 'Service'
KW_REPOSITORY_RESOURCE = 'Repository'
KW_HELPER_RESOURCE = 'Helper'
KW_CONVERTER_RESOURCE = 'Converter'
KW_RESOURCE_LIST = [
    KW_CONTROLLER_RESOURCE,
    KW_SERVICE_RESOURCE,
    KW_REPOSITORY_RESOURCE,
    KW_HELPER_RESOURCE,
    KW_CONVERTER_RESOURCE
]

DEFAULT_CONTENT_TYPE = 'application/json'
LOCALHOST_URL = 'http://127.0.0.1:5000'

def printMyStuff(stuff):
    print()
    print(f'    type(stuff).__name__ = {type(stuff).__name__}')
    print(f'    type(stuff).__class__.__name__ = {type(stuff).__class__.__name__}')
    print(f'    stuff.__class__.__name__ = {stuff.__class__.__name__}')
    print(f'    stuff.__class__.__module__ = {stuff.__class__.__module__}')
    print(f'    stuff.__class__.__qualname__ = {stuff.__class__.__qualname__}')

def printClass(Class) :
    print(f'{2 * Constant.TAB}Class.__name__ = {Class.__name__}')
    print(f'{2 * Constant.TAB}Class.__module__ = {Class.__module__}')
    print(f'{2 * Constant.TAB}Class.__qualname__ = {Class.__qualname__}')


class FlaskResource:
    ...

@Method
def jsonifyResponse(object, contentType, status) :
    return Response(Serializer.jsonifyIt(object),  mimetype = contentType, status = status)

@Method
def getClassName(instance) :
    return instance.__class__.__name__

@Method
def getModuleName(instance) :
    return instance.__class__.__module__

@Method
def getQualitativeName(instance) :
    return instance.__class__.__qualname__

@Method
def overrideSignatures(toOverride, original) :
    toOverride.__name__ = original.__name__
    toOverride.__module__ = original.__module__
    toOverride.__qualname__ = original.__qualname__

@Method
def appendedItInArgsAndReturnArgs(dto, args) :
    args = [arg for arg in args]
    args.append(dto)
    return tuple(arg for arg in args)

@Method
def getResourceName(resourceInstance) :
    return resourceInstance.__class__.__name__

@Method
def getResourceFinalName(resourceInstance, resourceName = None) :
    if not resourceName :
        resourceName = resourceInstance.__class__.__name__
    for kwAsset in KW_RESOURCE_LIST :
        if kwAsset in resourceName :
            resourceName = resourceName.replace(kwAsset, Constant.NOTHING)
    return f'{resourceName[0].lower()}{resourceName[1:]}'

@Method
def getResourceType(resourceInstance, resourceName = None) :
    if not resourceName :
        resourceName = resourceInstance.__class__.__name__
    for kwAsset in KW_RESOURCE_LIST :
        if kwAsset in resourceName :
            return kwAsset

@Method
def getAttributePointerList(object) :
    return [
        getattr(object, objectAttributeName)
        for objectAttributeName in dir(object)
        if (not objectAttributeName.startswith('__') and not objectAttributeName.startswith('_'))
    ]

@Method
def setMethod(resourceInstance, newMethod, methodName = None) :
    def buildNewClassMethod(resourceInstance, newMethod) :
        def myInnerMethod(*args, **kwargs) :
            return newMethod(resourceInstance,*args, **kwargs)
        overrideSignatures(myInnerMethod, newMethod)
        return myInnerMethod
    if not type(newMethod).__name__ == KW_METHOD :
        newMethod = buildNewClassMethod(resourceInstance, newMethod)
    if not methodName :
        methodName = newMethod.__name__
    setattr(resourceInstance, methodName, newMethod)
    return resourceInstance

@Method
def getGlobals() :
    try :
        from app import globals
    except Exception as exception :
        raise Exception('Failed to get "globals" instance from app.py')
    return globals

@Method
def getApi() :
    try:
        api = getGlobals().api
    except Exception as exception :
        raise Exception(f'Failed to return api from "globals" instance. Cause: {str(exception)}')
    return api

@Method
def validateFlaskApi(instance) :
    apiClassName = flask_restful.Api.__name__
    moduleName = flask_restful.__name__
    if not apiClassName == getClassName(instance) and apiClassName == getQualitativeName(instance) and moduleName == getModuleName(instance) :
        raise Exception(f'Globals can only be added to a "flask_restful.Api" instance. Not to {apiInstance}')

@Method
def addGlobalsTo(apiInstance) :
    validateFlaskApi(apiInstance)
    apiInstance.globals = getGlobals()
    apiInstance.globals.api = apiInstance
    apiInstance.bindResource = bindResource

@Method
def addResourceAttibutes(apiInstance) :
    setattr(apiInstance, KW_RESOURCE, FlaskResource())
    for resourceName in KW_RESOURCE_LIST :
        setattr(apiInstance.resource, resourceName.lower(), FlaskResource())

@Method
def addControllerListTo(apiInstance,controllerList) :
    for controller in controllerList :
        urlList = [controller.url]
        attributePointerList = getAttributePointerList(controller)
        for attributePointer in attributePointerList :
            if hasattr(attributePointer, KW_URL) and attributePointer.url :
                urlList.append(f'{controller.url}{attributePointer.url}')
        apiInstance.add_resource(controller, *urlList)

@Method
def addServiceListTo(apiInstance,serviceList) :
    for service in serviceList :
        apiInstance.bindResource(apiInstance,service())

@Method
def addRepositoryTo(apiInstance,repositoryList,model,localStorageName = None) :
    apiInstance.repository = SqlAlchemyHelper.SqlAlchemyHelper(
        localName = localStorageName if localStorageName else SqlAlchemyHelper.DEFAULT_LOCAL_STORAGE_NAME,
        model = model,
        globals = apiInstance.globals,
        echo = False,
        checkSameThread = False
    )
    for repository in repositoryList :
        apiInstance.bindResource(apiInstance,repository())

@Method
def addHelperListTo(apiInstance,helperList) :
    for helper in helperList :
        apiInstance.bindResource(apiInstance,helper())

@Method
def addConverterListTo(apiInstance,converterList) :
    for converter in converterList :
        apiInstance.bindResource(apiInstance,converter())

@Method
def addFlaskApiResources(
        apiInstance,
        controllerList,
        serviceList,
        repositoryList,
        helperList,
        converterList,
        model,
        localStorageName = None
    ) :
    addResourceAttibutes(apiInstance)
    addRepositoryTo(apiInstance,repositoryList,model,localStorageName = localStorageName)
    addServiceListTo(apiInstance,serviceList)
    addControllerListTo(apiInstance,controllerList)
    addHelperListTo(apiInstance,helperList)
    addConverterListTo(apiInstance,converterList)

@Method
def setResource(apiInstance,resourceInstance,resourceName = None) :
    resourceName = getResourceFinalName(resourceInstance,resourceName = resourceName)
    setattr(apiInstance,resourceName,resourceInstance)

@Method
def bindResource(apiInstance,resourceInstance) :
    validateFlaskApi(apiInstance)
    setResource(getattr(apiInstance.resource, getResourceType(resourceInstance).lower()), resourceInstance)

@Method
def initialize(defaultUrl = None) :
    defaultUrl = defaultUrl
    url = LOCALHOST_URL
    if defaultUrl :
        url = f'{url}{defaultUrl}'
    def inBetweenFunction(function,*argument,**keywordArgument) :
        noException = None
        log.wraper(initialize,f'''{function.__name__} method''',noException)
        # webbrowser.open_new(url)
        def innerFunction(*args,**kwargs) :
            try :
                return function(*args,**kwargs)
            except Exception as exception :
                raise Exception(f'Failed to initialize. Cause: {str(exception)}')
        return innerFunction
    return inBetweenFunction

@Method
def Controller(url = None) :
    controllerUrl = url
    def Wrapper(OuterClass,*args,**kwargs):
        apiInstance = getApi()
        noException = None
        log.wraper(Controller,f'''{OuterClass.__name__}''',noException)
        class InnerClass(OuterClass,flask_restful.Resource):
            url = controllerUrl
            def __init__(self,*args,**kwargs):
                OuterClass.__init__(self,*args,**kwargs)
                self.service = apiInstance.resource.service
                self.abort = abort
        overrideSignatures(InnerClass, OuterClass)
        return InnerClass
    return Wrapper

@Method
def ControllerMethod(url = None, bodyRequestClass = None, contentType = DEFAULT_CONTENT_TYPE):
    controllerMethodUrl = url
    def innerMethodWrapper(resourceInstanceMethod,*args,**kwargs) :
        noException = None
        log.wraper(ControllerMethod,f'''{resourceInstanceMethod.__name__}''',noException)
        def innerResourceInstanceMethod(*args,**kwargs) :
            self = args[0]
            if bodyRequestClass :
                bodyJson = request.get_json()
                dto = None if not bodyJson else Serializer.convertFromJsonToObject(bodyJson,bodyRequestClass)
                args = appendedItInArgsAndReturnArgs(dto, args)
            completeResponse = resourceInstanceMethod(self,*args[1:],**kwargs)
            controllerResponse = completeResponse[0]
            status = completeResponse[1]
            return jsonifyResponse(controllerResponse, contentType, status)
        overrideSignatures(innerResourceInstanceMethod, resourceInstanceMethod)
        innerResourceInstanceMethod.url = controllerMethodUrl
        return innerResourceInstanceMethod
    return innerMethodWrapper

@Method
def Service() :
    def Wrapper(OuterClass,*args,**kwargs):
        apiInstance = getApi()
        noException = None
        log.wraper(Service,f'''{OuterClass.__name__}''',noException)
        class InnerClass(OuterClass):
            def __init__(self,*args,**kwargs):
                OuterClass.__init__(self,*args,**kwargs)
                self.service = apiInstance.resource.service
                self.repository = apiInstance.resource.repository
                self.helper = apiInstance.resource.helper
                self.converter = apiInstance.resource.converter
                self.abort = abort
        overrideSignatures(InnerClass, OuterClass)
        return InnerClass
    return Wrapper

@Method
def Repository(model = None) :
    repositoryModel = model
    def Wrapper(OuterClass,*args,**kwargs):
        noException = None
        log.wraper(Repository,f'''{OuterClass.__name__}''',noException)
        class InnerClass(OuterClass):
            model = repositoryModel
            def __init__(self,*args,**kwargs):
                OuterClass.__init__(self,*args,**kwargs)
                self.repository = getApi().repository
                self.abort = abort
        overrideSignatures(InnerClass, OuterClass)
        return InnerClass
    return Wrapper

@Method
def Helper() :
    def Wrapper(OuterClass,*args,**kwargs):
        apiInstance = getApi()
        noException = None
        log.wraper(Helper,f'''{OuterClass.__name__}''',noException)
        class InnerClass(OuterClass,flask_restful.Resource):
            def __init__(self,*args,**kwargs):
                OuterClass.__init__(self,*args,**kwargs)
                self.helper = apiInstance.resource.helper
                self.converter = apiInstance.resource.converter
                self.abort = abort
        overrideSignatures(InnerClass, OuterClass)
        return InnerClass
    return Wrapper

@Method
def Converter() :
    def Wrapper(OuterClass,*args,**kwargs):
        apiInstance = getApi()
        noException = None
        log.wraper(Converter,f'''{OuterClass.__name__}''',noException)
        class InnerClass(OuterClass,flask_restful.Resource):
            def __init__(self,*args,**kwargs):
                OuterClass.__init__(self,*args,**kwargs)
                self.helper = apiInstance.resource.helper
                self.converter = apiInstance.resource.converter
                self.abort = abort
        overrideSignatures(InnerClass, OuterClass)
        return InnerClass
    return Wrapper

@Method
def ConverterMethod(objectClass = None, fromRequest = None) :
    def innerMethodWrapper(resourceInstanceMethod,*args,**kwargs) :
        noException = None
        log.wraper(ConverterMethod,f'''{resourceInstanceMethod.__name__}''',noException)
        def innerResourceInstanceMethod(*args,**kwargs) :
            if objectClass :
                self = args[0]
                dto = args[1]
                model = Serializer.convertFromObjectToObject(dto,objectClass)
                args = appendedItInArgsAndReturnArgs(model, args)
                return resourceInstanceMethod(self,dto,*args[2:],**kwargs)
            return resourceInstanceMethod(*args,**kwargs)
        overrideSignatures(innerResourceInstanceMethod, resourceInstanceMethod)
        return innerResourceInstanceMethod
    return innerMethodWrapper
