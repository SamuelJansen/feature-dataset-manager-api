from flask import send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from python_helper import Constant, log
import OpenApiBasic as basic
from OpenApiKey import Key as k
from OpenApiKey import HiddenKey as hk
from OpenApiValue import Value as v
from OpenApiKeyValue import KeyValue as kv

def addSwagger(appInstance, globals):
    SWAGGER_URL = '/swagger'
    API_URL = f'swagger.json'
    swaggerUi = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL
    )
    swaggerUi._static_folder = f'{globals.currentPath}api{globals.OS_SEPARATOR}resource{globals.OS_SEPARATOR}swaggerui{globals.OS_SEPARATOR}'
    appInstance.register_blueprint(swaggerUi, url_prefix=SWAGGER_URL)

################################################################################

def propertyElement(**kwargs):
    return basic.newByHiddenKey(hk.PROPERTY, **kwargs)

def propertyDict(name, **propertyElementDict):
    return basic.newByHiddenKeyValue(hk.PROPERTY, name, **propertyElementDict)

def definitionElement(**kwargs):
    return basic.newByHiddenKey(hk.DEFINITION, **kwargs)

def definitionDict(name, **definitionElementDict):
    return basic.newByHiddenKeyValue(hk.DEFINITION, name, **definitionElementDict)

def verbElement(name, **kwargs):
    return basic.newByHiddenKeyValue(hk.VERB, name, **kwargs)

def pathElement(name, **verbDict):
    return basic.newByHiddenKeyValue(hk.PATH, name, **verbDict)

################################################################################

def property(**kwargs):
    newKwargs = kwargs.copy()
    property = newKwargs.get(hk.PROPERTY)
    if property :
        del newKwargs[hk.PROPERTY]
    return propertyDict(property, **propertyElement(**newKwargs))

def properties(propertyDict):
    return basic.newByKeyDict(k.PROPERTIES, propertyDict)

def required(*requiredList):
    return basic.newListByKey(k.REQUIRED, *requiredList)

def definition(**kwargs):
    newKwargs = kwargs.copy()
    definition = newKwargs.get(hk.DEFINITION)
    if definition :
        del newKwargs[hk.DEFINITION]
    return propertyDict(definition, **definitionElement(**newKwargs))

def definitions(definitionDict):
    return basic.newByKeyDict(k.DEFINITIONS, definitionDict)

def verb(**kwargs):
    newKwargs = kwargs.copy()
    verb = newKwargs.get(hk.VERB)
    if verb :
        del newKwargs[hk.VERB]
    return verbElement(verb, **newKwargs)

def verbDict(**verbElementDict):
    return basic.newByHiddenKey(hk.VERBS, **verbElementDict)

def path(**verbDict):
    newVerbDict = verbDict.copy()
    path = newVerbDict.get(hk.PATH)
    if path :
        del newVerbDict[hk.PATH]
    return pathElement(path, **newVerbDict)

def paths(pathElementDict):
    return basic.newByKeyDict(k.PATHS, pathElementDict)

def tag(**kwargs):
    return basic.newByHiddenKey(hk.TAG, **kwargs)

def tags(*tagElementList):
    return basic.newListByKey(k.TAGS, *tagElementList)

def info(**kwargs):
    return basic.newByKey(k.INFO, **kwargs)

def swaggerDocumentation(**kwargs):
    return basic.newByHiddenKey(hk.SWAGGER_DOC, **kwargs)
