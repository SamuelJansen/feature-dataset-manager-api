import webbrowser
from python_helper import log, Constant
import flask_restful
from flask_restful import reqparse, abort
from flask import Response, request
from MethodWrapper import Method
import Serializer, SqlAlchemyHelper
import GlobalException, HttpStatus, ErrorLog

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
KW_DELETE = 'delete'

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
def appendedItInArgsAndReturnArgs(argument, args) :
    args = [arg for arg in args]
    args.append(argument)
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
        controllerList,
        serviceList,
        repositoryList,
        validatorList,
        mapperList,
        helperList,
        converterList,
        model,
        localStorageName = None
    ) :
    addResourceAttibutes(apiInstance)
    addRepositoryTo(apiInstance,repositoryList,model,localStorageName = localStorageName)
    addServiceListTo(apiInstance,serviceList)
    addControllerListTo(apiInstance,controllerList)
    addValidatorListTo(apiInstance,validatorList)
    addMapperListTo(apiInstance,mapperList)
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
def initialize(defaultUrl=None) :
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
def Controller(url=None) :
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
        overrideSignatures(InnerClass, OuterClass)
        return InnerClass
    return Wrapper

@Method
def ControllerMethod(url=None, requestClass=None, contentType=DEFAULT_CONTENT_TYPE):
    controllerMethodUrl = url
    def innerMethodWrapper(resourceInstanceMethod,*args,**kwargs) :
        noException = None
        log.wraper(ControllerMethod,f'''{resourceInstanceMethod.__name__}''',noException)
        def innerResourceInstanceMethod(*args,**kwargs) :
            self = args[0]
            try :
                if resourceInstanceMethod.__name__ == KW_POST or resourceInstanceMethod.__name__ == KW_PUT and requestClass :
                    bodyJson = request.get_json()
                    dto = None if not bodyJson else Serializer.convertFromJsonToObject(bodyJson,requestClass)
                    args = appendedItInArgsAndReturnArgs(dto, args)
                completeResponse = resourceInstanceMethod(self,*args[1:],**kwargs)
            except Exception as exception :
                log.error(self.__class__, f'Failed to excecute {resourceInstanceMethod.__name__} method', exception)

                # request.method:              GET
                # request.url:                 http://127.0.0.1:5000/alert/dingding/test?x=y
                # request.base_url:            http://127.0.0.1:5000/alert/dingding/test
                # request.url_charset:         utf-8
                # request.url_root:            http://127.0.0.1:5000/
                # str(request.url_rule):       /alert/dingding/test
                # request.host_url:            http://127.0.0.1:5000/
                # request.host:                127.0.0.1:5000
                # request.script_root:
                # request.path:                /alert/dingding/test
                # request.full_path:           /alert/dingding/test?x=y
                #
                # request.args:                ImmutableMultiDict([('x', 'y')])
                # request.args.get('x'):       y


                if not GlobalException.GlobalException.__name__ == exception.__class__.__name__ :
                    exception = GlobalException.GlobalException()
                try :
                    httpErrorLog = ErrorLog.ErrorLog()
                    httpErrorLog.override(exception)
                    api = getApi()
                    api.repository.saveAndCommit(httpErrorLog)
                except Exception as errorLogException :
                    log.error(self.__class__, f'Failed to persist {ErrorLog.ErrorLog.__name__}', errorLogException)
                completeResponse = [{'message':exception.message, 'url':exception.url},exception.status]
                log.error(self.__class__, f'Error processing {resourceInstanceMethod.__name__} request', exception)
            controllerResponse = completeResponse[0]
            status = completeResponse[1]
            return jsonifyResponse(controllerResponse, contentType, status)
        overrideSignatures(innerResourceInstanceMethod, resourceInstanceMethod)
        innerResourceInstanceMethod.url = controllerMethodUrl
        return innerResourceInstanceMethod
    return innerMethodWrapper

@Method
def validateArgs(args,requestClass,method) :
    if requestClass :
        self = args[0]
        if type(requestClass).__name__ == Constant.LIST :
            for index in range(len(requestClass)) :
                expecteObjectClass = requestClass[index]
                objectRequest = args[index + 1]
                if not expecteObjectClass.__name__ == objectRequest.__class__.__name__ :
                    raise GlobalException.GlobalException(logMessage = f'Invalid args. {self.__class__.__name__}.{method.__name__} call got an unnexpected object request: {objectRequest}. It should be {expecteObjectClass.__name__}')
        else :
            expecteObjectClass = requestClass
            objectRequest = args[1]
            if not requestClass.__name__ == objectRequest.__class__.__name__ :
                raise GlobalException.GlobalException(logMessage = f'Invalid args. {self.__class__.__name__}.{method.__name__} call got an unnexpected object request: {objectRequest}. It should be {expecteObjectClass.__name__}')

@Method
def Service() :
    def Wrapper(OuterClass, *args, **kwargs):
        apiInstance = getApi()
        noException = None
        log.wraper(Service,f'''{OuterClass.__name__}''',noException)
        class InnerClass(OuterClass):
            def __init__(self,*args,**kwargs):
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
        log.wraper(ServiceMethod,f'''{resourceInstanceMethod.__name__}''',noException)
        def innerResourceInstanceMethod(*args,**kwargs) :
            validateArgs(args,requestClass,innerResourceInstanceMethod)
            return resourceInstanceMethod(*args,**kwargs)
        overrideSignatures(innerResourceInstanceMethod, resourceInstanceMethod)
        return innerResourceInstanceMethod
    return innerMethodWrapper

@Method
def Repository(model = None) :
    repositoryModel = model
    def Wrapper(OuterClass, *args, **kwargs):
        noException = None
        log.wraper(Repository,f'''{OuterClass.__name__}''',noException)
        class InnerClass(OuterClass):
            model = repositoryModel
            def __init__(self,*args,**kwargs):
                OuterClass.__init__(self,*args,**kwargs)
                self.repository = getApi().repository
        overrideSignatures(InnerClass, OuterClass)
        return InnerClass
    return Wrapper

@Method
def Validator() :
    def Wrapper(OuterClass, *args, **kwargs):
        apiInstance = getApi()
        noException = None
        log.wraper(Validator,f'''{OuterClass.__name__}''',noException)
        class InnerClass(OuterClass,flask_restful.Resource):
            def __init__(self,*args,**kwargs):
                OuterClass.__init__(self,*args,**kwargs)
                self.validator = apiInstance.resource.validator
                self.helper = apiInstance.resource.helper
                self.converter = apiInstance.resource.converter
        overrideSignatures(InnerClass, OuterClass)
        return InnerClass
    return Wrapper

@Method
def ValidatorMethod(requestClass=None, message=None, logMessage=None, responseClass=None) :
    def innerMethodWrapper(resourceInstanceMethod,*args,**kwargs) :
        noException = None
        log.wraper(ValidatorMethod,f'''{resourceInstanceMethod.__name__}''',noException)
        def innerResourceInstanceMethod(*args,**kwargs) :
            validateArgs(args,requestClass,innerResourceInstanceMethod)
            # self = args[0]
            # if requestClass :
            #     objectRequest = args[1]
            #     if type(requestClass).__name__ == Constant.LIST :
            #         for index in range(len(requestClass)) :
            #             expecteObjectClass = requestClass[index]
            #             objectRequest = args[index + 1]
            #             if not requestClass[index].__name__ == objectRequest.__class__.__name__ :
            #                 raise GlobalException.GlobalException(logMessage = f'Invalid args. {self.__class__.__name__}.{innerResourceInstanceMethod.__name__} call got an unnexpected object request: {objectRequest}. It should be {expecteObjectClass.__name__}')
            #     else :
            #         expecteObjectClass = requestClass
            #         objectRequest = args[1]
            #         if not requestClass.__name__ == objectRequest.__class__.__name__ :
            #             raise GlobalException.GlobalException(logMessage = f'Invalid args. {self.__class__.__name__}.{innerResourceInstanceMethod.__name__} call got an unnexpected object request: {objectRequest}. It should be {expecteObjectClass.__name__}')
            #     # if not requestClass.__name__ == objectRequest.__class__.__name__ :
            #     #     raise GlobalException.GlobalException(
            #     #         message = message if message else None,
            #     #         logMessage = logMessage if logMessage else f"Validator error. {self.__class__.__name__}.{innerResourceInstanceMethod.__name__} call got an unnexpected object request: {objectRequest}",
            #     #         status = HttpStatus.BAD_REQUEST if message else None)
                # return resourceInstanceMethod(self,objectRequest,*args[2:],**kwargs)
            return resourceInstanceMethod(*args,**kwargs)
        overrideSignatures(innerResourceInstanceMethod, resourceInstanceMethod)
        return innerResourceInstanceMethod
    return innerMethodWrapper


@Method
def Mapper() :
    def Wrapper(OuterClass, *args, **kwargs):
        apiInstance = getApi()
        noException = None
        log.wraper(Mapper,f'''{OuterClass.__name__}''',noException)
        class InnerClass(OuterClass,flask_restful.Resource):
            def __init__(self,*args,**kwargs):
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
        log.wraper(MapperMethod,f'''{resourceInstanceMethod.__name__}''',noException)
        def innerResourceInstanceMethod(*args,**kwargs) :
            validateArgs(args,requestClass,innerResourceInstanceMethod)
            if responseClass :
                objectRequest = args[1]
                model = Serializer.convertFromObjectToObject(objectRequest,responseClass)
                args = appendedItInArgsAndReturnArgs(model, args)
            return resourceInstanceMethod(*args,**kwargs)
        overrideSignatures(innerResourceInstanceMethod, resourceInstanceMethod)
        return innerResourceInstanceMethod
    return innerMethodWrapper

@Method
def Helper() :
    def Wrapper(OuterClass, *args, **kwargs):
        apiInstance = getApi()
        noException = None
        log.wraper(Helper,f'''{OuterClass.__name__}''',noException)
        class InnerClass(OuterClass,flask_restful.Resource):
            def __init__(self,*args,**kwargs):
                OuterClass.__init__(self,*args,**kwargs)
                self.helper = apiInstance.resource.helper
                self.converter = apiInstance.resource.converter
        overrideSignatures(InnerClass, OuterClass)
        return InnerClass
    return Wrapper

@Method
def Converter() :
    def Wrapper(OuterClass, *args, **kwargs):
        apiInstance = getApi()
        noException = None
        log.wraper(Converter,f'''{OuterClass.__name__}''',noException)
        class InnerClass(OuterClass,flask_restful.Resource):
            def __init__(self,*args,**kwargs):
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
        log.wraper(ConverterMethod,f'''{resourceInstanceMethod.__name__}''',noException)
        def innerResourceInstanceMethod(*args,**kwargs) :
            validateArgs(args,requestClass,innerResourceInstanceMethod)
            if responseClass :
                self = args[0]
                objectRequest = args[1]
                model = Serializer.convertFromObjectToObject(objectRequest,responseClass)
                args = appendedItInArgsAndReturnArgs(model, args)
            return resourceInstanceMethod(*args,**kwargs)
        overrideSignatures(innerResourceInstanceMethod, resourceInstanceMethod)
        return innerResourceInstanceMethod
    return innerMethodWrapper
