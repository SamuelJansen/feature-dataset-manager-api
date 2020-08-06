import webbrowser
from python_helper import Constant, log
from flask import Response, request
import flask_restful
from MethodWrapper import Method, overrideSignatures
import Security, Serializer, OpenApiManager
import GlobalException, HttpStatus
import SqlAlchemyProxy

KW_URL = 'url'
KW_DEFAULT_URL = 'defaultUrl'
KW_MODEL = 'model'
KW_API = 'api'

KW_METHOD = 'method'

KW_RESOURCE = 'resource'

KW_CONTROLLER_RESOURCE = 'Controller'
KW_SERVICE_RESOURCE = 'Service'
KW_REPOSITORY_RESOURCE = 'Repository'
KW_VALIDATOR_RESOURCE = 'Validator'
KW_MAPPER_RESOURCE = 'Mapper'
KW_HELPER_RESOURCE = 'Helper'
KW_CONVERTER_RESOURCE = 'Converter'
KW_RESOURCE_LIST = [
    KW_CONTROLLER_RESOURCE,
    KW_SERVICE_RESOURCE,
    KW_REPOSITORY_RESOURCE,
    KW_VALIDATOR_RESOURCE,
    KW_MAPPER_RESOURCE,
    KW_HELPER_RESOURCE,
    KW_CONVERTER_RESOURCE
]

DEFAULT_CONTENT_TYPE = 'application/json'
LOCALHOST_URL = 'http://127.0.0.1:5000'

KW_GET = 'get'
KW_POST = 'post'
KW_PUT = 'put'
KW_PATCH = 'patch'
KW_DELETE = 'delete'

ABLE_TO_RECIEVE_BODY_LIST = [
    KW_POST,
    KW_PUT,
    KW_PATCH
]

DOT_SPACE_CAUSE = f'''{Constant.DOT_SPACE}{Constant.LOG_CAUSE}'''

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

def appendArgs(args, argument, isControllerMethod=False) :
    if isControllerMethod and Serializer.isList(argument) :
        return args + argument
    args.append(argument)
    return args

@Method
def getArgsWithSerializerReturnAppended(argument, args, isControllerMethod=False) :
    args = [arg for arg in args]
    args = appendArgs(args, argument, isControllerMethod=isControllerMethod)
    return tuple(arg for arg in args)

@Method
def getArgsWithResponseClassInstanceAppended(args, responseClass) :
    if responseClass :
        resourceInstance = args[0]
        objectRequest = args[1]
        serializerReturn = Serializer.convertFromObjectToObject(objectRequest, responseClass)
        args = getArgsWithSerializerReturnAppended(serializerReturn, args)
    return args

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
def getNullableApi() :
    try :
        api = getApi()
    except :
        api = None
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
def addControllerListTo(apiInstance, globalNamespace, controllerList) :
    for controller in controllerList :
        urlList = [controller.url]
        attributePointerList = getAttributePointerList(controller)
        for attributePointer in attributePointerList :
            if hasattr(attributePointer, KW_URL) and attributePointer.url :
                subUrlList = attributePointer.url.split(Constant.SLASH)
                concatenatedSubUrl = Constant.NOTHING
                for subUrl in subUrlList :
                    if subUrl :
                        concatenatedSubUrl += f'{Constant.SLASH}{subUrl}'
                        if '<' == subUrl[0] and '>' == subUrl[-1] :
                            urlList.append(f'{controller.url}{concatenatedSubUrl}')
        apiInstance.add_resource(controller, *urlList)

@Method
def addServiceListTo(apiInstance,serviceList) :
    for service in serviceList :
        apiInstance.bindResource(apiInstance,service())

@Method
def addRepositoryTo(apiInstance, repositoryList, model, databaseEnvironmentVariable=None, localStorageName=None) :
    apiInstance.repository = SqlAlchemyProxy.SqlAlchemyProxy(
        databaseEnvironmentVariable = databaseEnvironmentVariable,
        localName = localStorageName,
        model = model,
        globals = apiInstance.globals,
        echo = False,
        checkSameThread = False
    )
    for repository in repositoryList :
        apiInstance.bindResource(apiInstance,repository())

@Method
def addValidatorListTo(apiInstance,validatorList) :
    for validator in validatorList :
        apiInstance.bindResource(apiInstance,validator())

def addMapperListTo(apiInstance,mapperList) :
    for mapper in mapperList :
        apiInstance.bindResource(apiInstance,mapper())

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
        appInstance,
        globalNamespace,
        jwtInstance,
        controllerList,
        serviceList,
        repositoryList,
        validatorList,
        mapperList,
        helperList,
        converterList,
        model,
        databaseEnvironmentVariable = None,
        localStorageName = None
    ) :
    addResourceAttibutes(apiInstance)
    addRepositoryTo(apiInstance, repositoryList, model, databaseEnvironmentVariable=databaseEnvironmentVariable, localStorageName=localStorageName)
    addServiceListTo(apiInstance, serviceList)
    addControllerListTo(apiInstance, globalNamespace, controllerList)
    addValidatorListTo(apiInstance, validatorList)
    addMapperListTo(apiInstance, mapperList)
    addHelperListTo(apiInstance, helperList)
    addConverterListTo(apiInstance, converterList)
    Security.addJwt(jwtInstance)
    OpenApiManager.addSwagger(appInstance, apiInstance.globals)


@Method
def setResource(apiInstance,resourceInstance,resourceName = None) :
    resourceName = getResourceFinalName(resourceInstance,resourceName = resourceName)
    setattr(apiInstance,resourceName,resourceInstance)

@Method
def bindResource(apiInstance,resourceInstance) :
    validateFlaskApi(apiInstance)
    setResource(getattr(apiInstance.resource, getResourceType(resourceInstance).lower()), resourceInstance)

def getGlobalException(exception, resourceInstance, resourceInstanceMethod):
    apiInstance = getNullableApi()
    return GlobalException.handleLogErrorException(exception, resourceInstance, resourceInstanceMethod, apiInstance)

def raiseGlobalException(exception, resourceInstance, resourceInstanceMethod) :
    raise getGlobalException(exception, resourceInstance, resourceInstanceMethod)

@Method
def getCompleteResponseByException(exception, resourceInstance, resourceInstanceMethod) :
    exception = getGlobalException(exception, resourceInstance, resourceInstanceMethod)
    completeResponse = [{'message':exception.message, 'timestamp':str(exception.timeStamp)},exception.status]
    log.error(resourceInstance.__class__, f'Error processing {resourceInstance.__class__.__name__}.{resourceInstanceMethod.__name__} request', exception)
    return completeResponse

@Method
def initialize(defaultUrl=None) :
    defaultUrl = defaultUrl
    url = LOCALHOST_URL
    if defaultUrl :
        url = f'{url}{defaultUrl}'
    def inBetweenFunction(function,*argument,**keywordArgument) :
        noException = None
        log.debug(initialize,f'''{function.__name__} method''')
        webbrowser.open_new(url)
        def innerFunction(*args,**kwargs) :
            try :
                return function(*args,**kwargs)
            except Exception as exception :
                raise Exception(f'Failed to initialize. Cause: {str(exception)}')
        return innerFunction
    return inBetweenFunction

@Method
def Controller(url=None, description='Controller') :
    controllerUrl = url
    controllerDescription = description
    def Wrapper(OuterClass,*args,**kwargs):
        apiInstance = getApi()
        noException = None
        log.debug(Controller,f'''wrapping {OuterClass.__name__}''')
        class InnerClass(OuterClass,flask_restful.Resource):
            url = controllerUrl
            description = controllerDescription
            def __init__(self,*args,**kwargs):
                log.debug(OuterClass,f'in {InnerClass.__name__}.__init__(*{args},**{kwargs})')
                OuterClass.__init__(self)
                flask_restful.Resource.__init__(self,*args,**kwargs)
                self.service = apiInstance.resource.service
        overrideSignatures(InnerClass, OuterClass)
        return InnerClass
    return Wrapper

def getRequestBodyAsJson() :
    try :
        requestBodyAsJson = request.get_json()
    except Exception as exception :
        raise GlobalException.GlobalException(message='Not possible to parse the request', logMessage=str(exception), status=HttpStatus.BAD_REQUEST)
    return requestBodyAsJson

@Security.jwtRequired
def securedMethod(args, kwargs, resourceInstance, resourceInstanceMethod, requestClass, roleRequired) :
    if not Security.getRole() in roleRequired :
        raise GlobalException.GlobalException(message='Role not allowed', logMessage=f'''Role {Security.getRole()} trying to access denied resourse''', status=HttpStatus.FORBIDEN)
    return notSecuredMethod(args, kwargs, resourceInstance, resourceInstanceMethod, requestClass)

def notSecuredMethod(args, kwargs, resourceInstance, resourceInstanceMethod, requestClass) :
    if resourceInstanceMethod.__name__ in ABLE_TO_RECIEVE_BODY_LIST and requestClass :
        requestBodyAsJson = getRequestBodyAsJson() ###- request.get_json()
        if requestBodyAsJson :
            serializerReturn = Serializer.convertFromJsonToObject(requestBodyAsJson, requestClass)
            args = getArgsWithSerializerReturnAppended(serializerReturn, args, isControllerMethod=True)
    return resourceInstanceMethod(resourceInstance,*args[1:],**kwargs)

@Method
def ControllerMethod(url=None, requestClass=None, roleRequired=None, contentType=DEFAULT_CONTENT_TYPE):
    controllerMethodUrl = url
    def innerMethodWrapper(resourceInstanceMethod,*args,**kwargs) :
        noException = None
        log.debug(ControllerMethod,f'''wrapping {resourceInstanceMethod.__name__}''')
        def innerResourceInstanceMethod(*args,**kwargs) :
            resourceInstance = args[0]
            try :
                if roleRequired and (type(list()) == type(roleRequired) and not [] == roleRequired) :
                    completeResponse = securedMethod(args, kwargs, resourceInstance, resourceInstanceMethod, requestClass, roleRequired)
                else :
                    completeResponse = notSecuredMethod(args, kwargs, resourceInstance, resourceInstanceMethod, requestClass)
            except Exception as exception :
                completeResponse = getCompleteResponseByException(exception, resourceInstance, resourceInstanceMethod)
                ###- request.method:              GET
                ###- request.url:                 http://127.0.0.1:5000/alert/dingding/test?x=y
                ###- request.base_url:            http://127.0.0.1:5000/alert/dingding/test
                ###- request.url_charset:         utf-8
                ###- request.url_root:            http://127.0.0.1:5000/
                ###- str(request.url_rule):       /alert/dingding/test
                ###- request.host_url:            http://127.0.0.1:5000/
                ###- request.host:                127.0.0.1:5000
                ###- request.script_root:
                ###- request.path:                /alert/dingding/test
                ###- request.full_path:           /alert/dingding/test?x=y
                ###- request.args:                ImmutableMultiDict([('x', 'y')])
                ###- request.args.get('x'):       y
            controllerResponse = completeResponse[0]
            status = completeResponse[1]
            return jsonifyResponse(controllerResponse, contentType, status)
        overrideSignatures(innerResourceInstanceMethod, resourceInstanceMethod)
        innerResourceInstanceMethod.url = controllerMethodUrl
        return innerResourceInstanceMethod
    return innerMethodWrapper

@Method
def validateArgs(args, requestClass, method) :
    if requestClass :
        resourceInstance = args[0]
        if Serializer.isList(requestClass) :
            for index in range(len(requestClass)) :
                if Serializer.isList(args[index + 1]) and len(args[index + 1]) > 0 :
                    expecteObjectClass = requestClass[index][0]
                    for objectInstance in args[index + 1] :
                        GlobalException.validateArgs(resourceInstance, method, objectInstance, expecteObjectClass)
                else :
                    objectRequest = args[index + 1]
                    expecteObjectClass = requestClass[index]
                    GlobalException.validateArgs(resourceInstance, method, objectRequest, expecteObjectClass)
        else :
            objectRequest = args[1]
            expecteObjectClass = requestClass
            GlobalException.validateArgs(resourceInstance, method, objectRequest, expecteObjectClass)

@Method
def Service() :
    def Wrapper(OuterClass, *args, **kwargs):
        apiInstance = getApi()
        noException = None
        log.debug(Service,f'''wrapping {OuterClass.__name__}''')
        class InnerClass(OuterClass):
            def __init__(self,*args,**kwargs):
                log.debug(OuterClass,f'in {InnerClass.__name__}.__init__(*{args},**{kwargs})')
                OuterClass.__init__(self,*args,**kwargs)
                self.service = apiInstance.resource.service
                self.repository = apiInstance.resource.repository
                self.validator = apiInstance.resource.validator
                self.mapper = apiInstance.resource.mapper
                self.helper = apiInstance.resource.helper
                self.converter = apiInstance.resource.converter
        overrideSignatures(InnerClass, OuterClass)
        return InnerClass
    return Wrapper

@Method
def ServiceMethod(requestClass=None):
    def innerMethodWrapper(resourceInstanceMethod,*args,**kwargs) :
        noException = None
        log.debug(ServiceMethod,f'''innerMethodWrapper wraped {resourceInstanceMethod.__name__}''')
        def innerResourceInstanceMethod(*args,**kwargs) :
            resourceInstance = args[0]
            try :
                validateArgs(args,requestClass,innerResourceInstanceMethod)
                methodReturn = resourceInstanceMethod(*args,**kwargs)
            except Exception as exception :
                raiseGlobalException(exception, resourceInstance, resourceInstanceMethod)
            return methodReturn
        overrideSignatures(innerResourceInstanceMethod, resourceInstanceMethod)
        return innerResourceInstanceMethod
    return innerMethodWrapper

@Method
def Repository(model = None) :
    repositoryModel = model
    def Wrapper(OuterClass, *args, **kwargs):
        apiInstance = getApi()
        noException = None
        log.debug(Repository,f'''wrapping {OuterClass.__name__}''')
        class InnerClass(OuterClass):
            model = repositoryModel
            def __init__(self,*args,**kwargs):
                log.debug(OuterClass,f'in {InnerClass.__name__}.__init__(*{args},**{kwargs})')
                OuterClass.__init__(self,*args,**kwargs)
                self.repository = apiInstance.repository
        overrideSignatures(InnerClass, OuterClass)
        return InnerClass
    return Wrapper

@Method
def Validator() :
    def Wrapper(OuterClass, *args, **kwargs):
        apiInstance = getApi()
        noException = None
        log.debug(Validator,f'''wrapping {OuterClass.__name__}''')
        class InnerClass(OuterClass):
            def __init__(self,*args,**kwargs):
                log.debug(OuterClass,f'in {InnerClass.__name__}.__init__(*{args},**{kwargs})')
                OuterClass.__init__(self,*args,**kwargs)
                self.service = apiInstance.resource.service
                self.validator = apiInstance.resource.validator
                self.helper = apiInstance.resource.helper
                self.converter = apiInstance.resource.converter
        overrideSignatures(InnerClass, OuterClass)
        return InnerClass
    return Wrapper

@Method
def ValidatorMethod(requestClass=None, message=None, logMessage=None) :
    def innerMethodWrapper(resourceInstanceMethod,*args,**kwargs) :
        noException = None
        log.debug(ValidatorMethod,f'''wrapping {resourceInstanceMethod.__name__}''')
        def innerResourceInstanceMethod(*args,**kwargs) :
            resourceInstance = args[0]
            try :
                validateArgs(args,requestClass,innerResourceInstanceMethod)
                methodReturn = resourceInstanceMethod(*args,**kwargs)
            except Exception as exception :
                raiseGlobalException(exception, resourceInstance, resourceInstanceMethod)
            return methodReturn
        overrideSignatures(innerResourceInstanceMethod, resourceInstanceMethod)
        return innerResourceInstanceMethod
    return innerMethodWrapper


@Method
def Mapper() :
    def Wrapper(OuterClass, *args, **kwargs):
        apiInstance = getApi()
        noException = None
        log.debug(Mapper,f'''wrapping {OuterClass.__name__}''')
        class InnerClass(OuterClass):
            def __init__(self,*args,**kwargs):
                log.debug(OuterClass,f'in {InnerClass.__name__}.__init__(*{args},**{kwargs})')
                OuterClass.__init__(self,*args,**kwargs)
                self.service = apiInstance.resource.service
                self.validator = apiInstance.resource.validator
                self.mapper = apiInstance.resource.mapper
                self.helper = apiInstance.resource.helper
                self.converter = apiInstance.resource.converter
        overrideSignatures(InnerClass, OuterClass)
        return InnerClass
    return Wrapper

@Method
def MapperMethod(requestClass=None, responseClass=None) :
    def innerMethodWrapper(resourceInstanceMethod,*args,**kwargs) :
        noException = None
        log.debug(MapperMethod,f'''wrapping {resourceInstanceMethod.__name__}''')
        def innerResourceInstanceMethod(*args,**kwargs) :
            resourceInstance = args[0]
            try :
                validateArgs(args,requestClass,innerResourceInstanceMethod)
                args = getArgsWithResponseClassInstanceAppended(args, responseClass)
                methodReturn = resourceInstanceMethod(*args,**kwargs)
            except Exception as exception :
                raiseGlobalException(exception, resourceInstance, resourceInstanceMethod)
            return methodReturn
        overrideSignatures(innerResourceInstanceMethod, resourceInstanceMethod)
        return innerResourceInstanceMethod
    return innerMethodWrapper

@Method
def Helper() :
    def Wrapper(OuterClass, *args, **kwargs):
        apiInstance = getApi()
        noException = None
        log.debug(Helper,f'''wrapping {OuterClass.__name__}''')
        class InnerClass(OuterClass,flask_restful.Resource):
            def __init__(self,*args,**kwargs):
                log.debug(OuterClass,f'in {InnerClass.__name__}.__init__(*{args},**{kwargs})')
                OuterClass.__init__(self,*args,**kwargs)
                self.helper = apiInstance.resource.helper
                self.converter = apiInstance.resource.converter
        overrideSignatures(InnerClass, OuterClass)
        return InnerClass
    return Wrapper

@Method
def HelperMethod(requestClass=None, responseClass=None) :
    def innerMethodWrapper(resourceInstanceMethod,*args,**kwargs) :
        noException = None
        log.debug(HelperMethod,f'''wrapping {resourceInstanceMethod.__name__}''')
        def innerResourceInstanceMethod(*args,**kwargs) :
            resourceInstance = args[0]
            try :
                validateArgs(args,requestClass,innerResourceInstanceMethod)
                args = getArgsWithResponseClassInstanceAppended(args, responseClass)
                methodReturn = resourceInstanceMethod(*args,**kwargs)
            except Exception as exception :
                raiseGlobalException(exception, resourceInstance, resourceInstanceMethod)
            return methodReturn
        overrideSignatures(innerResourceInstanceMethod, resourceInstanceMethod)
        return innerResourceInstanceMethod
    return innerMethodWrapper

@Method
def Converter() :
    def Wrapper(OuterClass, *args, **kwargs):
        apiInstance = getApi()
        noException = None
        log.debug(Converter,f'''wrapping {OuterClass.__name__}''')
        class InnerClass(OuterClass):
            def __init__(self,*args,**kwargs):
                log.debug(OuterClass,f'in {InnerClass.__name__}.__init__(*{args},**{kwargs})')
                OuterClass.__init__(self,*args,**kwargs)
                self.helper = apiInstance.resource.helper
                self.converter = apiInstance.resource.converter
        overrideSignatures(InnerClass, OuterClass)
        return InnerClass
    return Wrapper

@Method
def ConverterMethod(requestClass=None, responseClass=None) :
    def innerMethodWrapper(resourceInstanceMethod,*args,**kwargs) :
        noException = None
        log.debug(ConverterMethod,f'''wrapping {resourceInstanceMethod.__name__}''')
        def innerResourceInstanceMethod(*args,**kwargs) :
            resourceInstance = args[0]
            try :
                validateArgs(args, requestClass, innerResourceInstanceMethod)
                args = getArgsWithResponseClassInstanceAppended(args, responseClass)
                methodReturn = resourceInstanceMethod(*args,**kwargs)
            except Exception as exception :
                raiseGlobalException(exception, resourceInstance, resourceInstanceMethod)
            return methodReturn
        overrideSignatures(innerResourceInstanceMethod, resourceInstanceMethod)
        return innerResourceInstanceMethod
    return innerMethodWrapper
