import json, importlib
from python_helper import Constant, log
from MethodWrapper import Method
from SqlAlchemyHelper import DeclarativeMeta

IGNORE_REOURCE_LIST = [
    'FlaskHelper',
    'MethodWrapper',
    'ResourceHelper',
    'SqlAlchemyHelper'
]

EXPAND_ALL_FIELDS = 'EXPAND_ALL_FIELDS'

DTO_CLASS_ROLE = 'DTO'
MODEL_CLASS_ROLE = 'MODEL'

DTO_SUFIX = 'Dto'
LIST_SUFIX = 'List'

@Method
def importResource(resourceName, resourceFileName = None) :
    if not resourceName in IGNORE_REOURCE_LIST :
        resource = None
        if not resourceFileName :
            resourceFileName = resourceName
        try :
            module = __import__(resourceFileName)
        except :
            module = importlib.import_module(resourceFileName)
        try :
            resource = getattr(module, resourceName)
        except Exception as exception :
            log.warning(importResource, f'Not possible to import {resourceName} from {resourceFileName}. cause: {str(exception)}')
        return resource

@Method
def importResourceList(resourceName) :
    import FlaskHelper
    def getControllerNameList(controllerName) :
        controllerNameList = [controllerName]
        controllerNameList.append(f'{controllerName[:-len(FlaskHelper.KW_CONTROLLER_RESOURCE)]}s{FlaskHelper.KW_CONTROLLER_RESOURCE}')
        return controllerNameList
    if FlaskHelper.KW_CONTROLLER_RESOURCE == resourceName[-len(FlaskHelper.KW_CONTROLLER_RESOURCE):] :
        controllerNameList = getControllerNameList(resourceName)
        importedResourceList = []
        for controllerName in controllerNameList :
            resource = importResource(controllerName, resourceFileName = resourceName)
            if resource :
                importedResourceList.append(resource)
        return importedResourceList
    resource = importResource(resourceName)
    if resource :
        return [resource]

@Method
def isSerializable(attributeValue) :
    return (isinstance(attributeValue.__class__, DeclarativeMeta) or
        (isinstance(attributeValue, list) and len(attributeValue) > 0 and isinstance(attributeValue[0].__class__, DeclarativeMeta)))

@Method
def getAttributeSet(object, fieldsToExpand, classTree, verifiedClassList) :
    attributeSet = {}
    presentClass = object.__class__.__name__
    if presentClass not in classTree :
        classTree[presentClass] = [object]
    elif classTree[presentClass].count(object) < 2 :
        classTree[presentClass].append(object)
    for attributeName in [name for name in dir(object) if not name.startswith('_') and not name == 'metadata']:
        attributeValue = object.__getattribute__(attributeName)
        if classTree[presentClass].count(object) > 1 :
            attributeSet[attributeName] = None
            continue
        if isSerializable(attributeValue) :
            if attributeName not in fieldsToExpand :
                if EXPAND_ALL_FIELDS not in fieldsToExpand :
                    attributeSet[attributeName] = None
                    continue
        attributeSet[attributeName] = attributeValue
    return attributeSet

@Method
def getJsonifier(revisitingItself = False, fieldsToExpand = [EXPAND_ALL_FIELDS], classTree = None, verifiedClassList = None):
    visitedObjectList = []
    class SqlAlchemyJsonifier(json.JSONEncoder):
        def default(self, object):
            if isinstance(object.__class__, DeclarativeMeta) :
                if revisitingItself :
                    if object in visitedObjectList:
                        return
                    visitedObjectList.append(object)
                if object.__class__.__name__ in classTree and classTree[object.__class__.__name__].count(object) > 0 :
                    return
                return getAttributeSet(object, fieldsToExpand, classTree, verifiedClassList)
            try :
                objectDefaultlyEncoded = json.JSONEncoder.default(self, object)
            except Exception as exception :
                try :
                    objectDefaultlyEncoded = object.__dict__
                except Exception as otherException :
                    raise Exception(f'Failed to encode object. Cause {str(exception)} and {str(otherException)}')
            return objectDefaultlyEncoded
    return SqlAlchemyJsonifier

@Method
def jsonifyIt(object, fieldsToExpand = [EXPAND_ALL_FIELDS]) :
    jsonCompleted = json.dumps(object, cls = getJsonifier(classTree = {}, verifiedClassList = []), check_circular = False)
    return jsonCompleted.replace('}, null]','}]').replace('[null]','[]')

@Method
def instanciateIt(objectClass) :
    args = []
    for ammountOfVariables in range(60) :
        try :
            objectInstance = objectClass(*args)
            break
        except Exception as exception :
            args.append(None)
        raise Exception(f'Not possible to instanciate {objectClass} class. Cause: {str(exception)}')
    return objectInstance

@Method
def getAttributeNameList(objectClass) :
    object = instanciateIt(objectClass)
    return [
        objectAttributeName
        for objectAttributeName in dir(object)
        if (not objectAttributeName.startswith('__') and not objectAttributeName.startswith('_'))
    ]

def isDictionary(thing) :
    return type(thing).__name__ == Constant.DICT


def isList(thing) :
    return type(thing).__name__ == Constant.LIST

@Method
def getClassRole(objectClass) :
    if DTO_SUFIX == objectClass.__name__[-3:] :
        return DTO_CLASS_ROLE
    return MODEL_CLASS_ROLE

@Method
def getResourceName(key, classRole) :
    capitalizedKey = f'{key[0].upper()}{key[1:]}'
    if DTO_CLASS_ROLE == classRole :
        return f'{capitalizedKey}{DTO_SUFIX}'
    return capitalizedKey

@Method
def resolveValue(value, key, classRole) :
    # print(f'        isList({value}) = {isList(value)}')
    if isList(value) :
        if LIST_SUFIX == key[-4:] :
            keyClass = importResource(getResourceName(key[:-4], classRole))
            # print(f'                keyClass = {keyClass.__name__}')
            convertedValue = []
            for jsonItem in value :
                if jsonItem :
                    convertedItem = convertFromJsonToObject(jsonItem,keyClass)
                    convertedValue.append(convertedItem)
            return convertedValue
    return value

@Method
def convertFromJsonToObject(fromJson,toObjectClass) :
    classRole = getClassRole(toObjectClass)
    attributeNameList = getAttributeNameList(toObjectClass)

    # print(f'        attributeNameList = {attributeNameList}')

    fromJsonToDictionary = {}
    for attributeName in attributeNameList :
        # print(f'        fromJson.get({attributeName}) = {fromJson.get(attributeName)}')
        jsonAttributeValue = fromJson.get(attributeName)
        if jsonAttributeValue :
            fromJsonToDictionary[attributeName] = resolveValue(jsonAttributeValue, attributeName, classRole)
        # if jsonAttributeValue :
        #     setattr(fromObject, attributeName, jsonAttributeValue)
    # print(f'        fromJsonToDictionary = {fromJsonToDictionary}')
    return toObjectClass(**fromJsonToDictionary)

@Method
def convertFromObjectToObject(fromObject,toObjectClass) :
    fromJson = json.loads(jsonifyIt(fromObject))
    # print(f'        fromJson = {fromJson}')
    return convertFromJsonToObject(fromJson,toObjectClass)
