from flask import send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from python_helper import Constant as c
from python_helper import log, StringHelper
import Serializer
from OpenApiKey import Key as k
from OpenApiValue import Value as v
import OpenApiDocumentationFile

KW_GET = 'get'
KW_POST = 'post'
KW_PUT = 'put'
KW_PATCH = 'patch'
KW_DELETE = 'delete'

VERB_LIST = [
    KW_GET,
    KW_POST,
    KW_PUT,
    KW_PATCH,
    KW_DELETE
]

ABLE_TO_RECIEVE_BODY_LIST = [
    KW_POST,
    KW_PUT,
    KW_PATCH
]

DEFAULT_CONTENT_TYPE = 'application/json'

KW_API = 'api'
KW_INFO = 'info'
KW_DESCRIPTION = 'description'
KW_TITLE = 'title'
KW_VERSION = 'version'
KW_TERMS_OF_SERVICE = 'terms-of-service'
KW_CONTACT = 'contact'
KW_LICENSE = 'license'
KW_NAME = 'name'
KW_EMAIL = 'email'
KW_URL = 'url'

KW_URL_SET = '__URL_SET__'
KW_DESCRIPTION_LIST = '__DESCRIPTION_LIST__'
KW_CONTROLLER = '__CONTROLLER__'
KW_METHOD = '__METHOD__'

def addSwagger(appInstance, apiInstance):
    g = apiInstance.globals
    SWAGGER_URL = '/swagger'
    API_URL = f'swagger.json'
    swaggerUi = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL
    )
    swaggerUi._static_folder = f'{g.currentPath}api{g.OS_SEPARATOR}resource{g.OS_SEPARATOR}swaggerui{g.OS_SEPARATOR}'
    appInstance.register_blueprint(swaggerUi, url_prefix=SWAGGER_URL)

################################################################################

def newDocumentation(apiInstance, appInstance):
    documentation = {
        k.SWAGGER_VERSION : v.SWAGGER_VERSION
    }
    apiInstance.documentation = documentation
    addHostAndBasePath(apiInstance, appInstance)
    addInfo(apiInstance)
    OpenApiDocumentationFile.overrideDocumentation(apiInstance.globals, documentation)

def addInfo(apiInstance):
    g = apiInstance.globals
    apiInstance.documentation[k.INFO] = {}
    apiInstance.documentation[k.INFO][k.TITLE] = g.getApiSetting(f'{KW_API}.{KW_INFO}.{KW_TITLE}')
    apiInstance.documentation[k.INFO][k.DESCRIPTION] = g.getApiSetting(f'{KW_API}.{KW_INFO}.{KW_DESCRIPTION}')
    apiInstance.documentation[k.INFO][k.VERSION] = g.getApiSetting(f'{KW_API}.{KW_INFO}.{KW_VERSION}')
    apiInstance.documentation[k.INFO][k.TERMS_OF_SERVICE] = g.getApiSetting(f'{KW_API}.{KW_INFO}.{KW_TERMS_OF_SERVICE}')
    addContact(g, apiInstance.documentation)
    addLisence(g, apiInstance.documentation)

def addHostAndBasePath(apiInstance, appInstance):
    apiInstance.documentation[k.HOST] = appInstance.test_request_context().request.host_url[:-1] ###- request.remote_addr
    if 'localhost' in apiInstance.documentation[k.HOST] :
        apiInstance.documentation[k.HOST] = f'{apiInstance.documentation[k.HOST]}:5000'
    apiInstance.documentation[k.BASE_PATH] = apiInstance.baseUrl
    apiInstance.documentation[k.SCHEMES] = [apiInstance.documentation[k.HOST].split('://')[0]]

# def addTagsPathsAndDefinitions(apiInstance):
#     COMA_SPACE = ', '
#     g = apiInstance.globals
#     controllerSet = apiInstance.resource.controllerSet
#     documentation = OpenApiDocumentationFile.loadDocumentation(g)
#     documentation[k.PATHS] = {}
#     documentation[k.DEFINITIONS] = {}
#     for key,value in controllerSet.items() :
#         # documentation[k.TAGS].append({
#         #     k.NAME : key,
#         #     k.DESCRIPTION : COMA_SPACE.join(value[KW_DESCRIPTION_LIST]),
#         #     k.EXTERNAL_DOCS : value.get(k.EXTERNAL_DOCS)
#         # })
#         for item in value[KW_URL_SET].values() :
#             for verb, verbContent in item.items() :
#                 url = verbContent[KW_URL]
#                 addUrlIfNeeded(url, documentation)
#                 if verb in [KW_GET, KW_POST, KW_PUT, KW_DELETE, KW_PATCH] :
#                     addVerb(verb, url, documentation)
#
#                     controller = verbContent[KW_CONTROLLER]
#                     method = verbContent[KW_METHOD]
#
#                     if not k.TAGS in documentation[k.PATHS][url][verb] :
#                         documentation[k.PATHS][url][verb][k.TAGS] = []
#                     if not key in documentation[k.PATHS][url][verb][k.TAGS] :
#                         documentation[k.PATHS][url][verb][k.TAGS].append(key)
#
#                     if not k.CONSUMES in documentation[k.PATHS][url][verb] :
#                         documentation[k.PATHS][url][verb][k.CONSUMES] = []
#                     if not k.PRODUCES in documentation[k.PATHS][url][verb] :
#                         documentation[k.PATHS][url][verb][k.PRODUCES] = []
#                     if not method.consumes in documentation[k.PATHS][url][verb][k.CONSUMES] :
#                         documentation[k.PATHS][url][verb][k.CONSUMES].append(method.consumes)
#                     if not method.produces in documentation[k.PATHS][url][verb][k.PRODUCES] :
#                         documentation[k.PATHS][url][verb][k.PRODUCES].append(method.produces)
#
#                     if k.PARAMETERS not in documentation[k.PATHS][url][verb] :
#                         documentation[k.PATHS][url][verb][k.PARAMETERS] = []
#
#                     requestClass = method.requestClass
#                     if requestClass :
#                         if not isinstance(requestClass, list) or (len(requestClass) == 1 and not isinstance(requestClass[0], list)) :
#                             if not requestClass.__name__ in documentation[k.DEFINITIONS] :
#                                 requestClassDoc = {}
#                                 documentation[k.DEFINITIONS][requestClass.__name__] = requestClassDoc
#                                 requestClassDoc[k.TYPE] = v.OBJECT
#                                 requestClassDoc[k.PROPERTIES] = {}
#                                 requestClassDoc[k.REQUIRED] = Serializer.getAttributeNameList(requestClass)
#                                 for attributeName in requestClassDoc[k.REQUIRED] :
#                                     requestClassDoc[k.PROPERTIES][attributeName] = {
#                                         k.TYPE : c.NULL_VALUE
#                                     }
#                     if c.LESSER in url :
#                         attributeList = url.split(c.LESSER)
#                         for attributeUrl in attributeList :
#                             if c.BIGGER in attributeUrl :
#                                 attributeUrl = attributeUrl.split(c.BIGGER)[0]
#                                 attributeUrlNameAndType = attributeUrl.split(c.COLON)
#                                 documentation[k.PATHS][url][verb][k.PARAMETERS].append({
#                                     k.NAME : attributeUrlNameAndType[1],
#                                     k.TYPE : attributeUrlNameAndType[0],
#                                     k.IN : v.PATH,
#                                     k.REQUIRED: True
#                                 })
#     print(StringHelper.stringfyThisDictionary(controllerSet))

def addControllerDocumentation(controller, apiInstance) :
    if not controller.tag in getTagNameList(apiInstance.documentation) :
        apiInstance.documentation[k.TAGS].append({
            k.NAME : controller.tag,
            k.DESCRIPTION : [controller.description],
            k.EXTERNAL_DOCS : None
        })
    OpenApiDocumentationFile.overrideDocumentation(apiInstance.globals, apiInstance.documentation)

################################################################################

def getTagNameList(documentation):
    if k.TAGS not in documentation :
        documentation[k.TAGS] = []
    tagNameList = []
    for tag in documentation[k.TAGS] :
        tagNameList.append(tag[k.NAME])
    return tagNameList

def addContact(globals, documentation):
    g = globals
    documentation[k.INFO][k.CONTACT] = {}
    documentation[k.INFO][k.CONTACT][k.NAME] = g.getApiSetting(f'{KW_API}.{KW_INFO}.{KW_CONTACT}.{KW_NAME}')
    documentation[k.INFO][k.CONTACT][k.EMAIL] = g.getApiSetting(f'{KW_API}.{KW_INFO}.{KW_CONTACT}.{KW_EMAIL}')

def addLisence(globals, documentation):
    g = globals
    documentation[k.INFO][k.LICENSE] = {}
    documentation[k.INFO][k.LICENSE][k.NAME] = g.getApiSetting(f'{KW_API}.{KW_INFO}.{KW_LICENSE}.{KW_NAME}')
    documentation[k.INFO][k.LICENSE][k.URL] = g.getApiSetting(f'{KW_API}.{KW_INFO}.{KW_LICENSE}.{KW_URL}')

def addUrlIfNeeded(url, documentation):
    existingUrl = documentation[k.PATHS].get(url)
    if not existingUrl :
        documentation[k.PATHS][url] = {}

def addVerb(verb, url, documentation):
    existingVerb = documentation[k.PATHS][url].get(verb)
    if not existingVerb :
        documentation[k.PATHS][url][verb] = {}
    else :
        raise Exception(f'Duplicated "{verb}" verb in {url} url')
