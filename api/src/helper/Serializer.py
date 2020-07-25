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

POST_VERB = 'Post'
PUT_VERB = 'Put'
GET_VERB = 'GET'
DELETE_VERB = 'Delete'

CREATE_ACTION = 'Create'
UPDATE_ACTION = 'Update'
QUERY_ACTION = 'Query'
DELETE_ACTION = 'Delete'

MESO_SUFIX_LIST = [
    POST_VERB,
    PUT_VERB,
    GET_VERB,
    DELETE_VERB,
    CREATE_ACTION,
    UPDATE_ACTION,
    QUERY_ACTION,
    DELETE_ACTION
]


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
    for attributeName in [name for name in dir(object) if not name.startswith(Constant.UNDERSCORE) and not name == 'metadata']:
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
def instanciateItWithNoArgsConstructor(objectClass) :
    args = []
    objectInstance = None
    for ammountOfVariables in range(60) :
        try :
            objectInstance = objectClass(*args)
            break
        except :
            args.append(None)
    if not objectInstance :
        raise Exception(f'Not possible to instanciate {objectClass} class in instanciateItWithNoArgsConstructor() method')
    return objectInstance

@Method
def getAttributeNameList(objectClass) :
    object = instanciateItWithNoArgsConstructor(objectClass)
    return [
        objectAttributeName
        for objectAttributeName in dir(object)
        if (not objectAttributeName.startswith(f'{2 * Constant.UNDERSCORE}') and not objectAttributeName.startswith(Constant.UNDERSCORE))
    ]

def isDictionary(thing) :
    return type(thing).__name__ == Constant.DICT


def isList(thing) :
    return type(thing).__name__ == Constant.LIST

@Method
def getClassRole(objectClass) :
    if DTO_SUFIX == objectClass.__name__[-len(DTO_SUFIX):] :
        for mesoSufix in MESO_SUFIX_LIST :
            if mesoSufix == objectClass.__name__[-len(mesoSufix):-len(DTO_SUFIX)] :
                return f'{mesoSufix}{Constant.UNDERSCORE}{DTO_SUFIX}'
        return DTO_CLASS_ROLE
    return MODEL_CLASS_ROLE

@Method
def getResourceName(key, classRole) :
    resourceName = f'{key[0].upper()}{key[1:]}'
    if DTO_CLASS_ROLE in classRole :
        sufixResourceNameList = classRole.lower().split(Constant.UNDERSCORE)
        for sufix in sufixResourceNameList :
            resourceName += f'{sufix[0].upper()}{sufix[1:]}'
        return resourceName
    return resourceName

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

    ###- bug detected

    attributeNameList = getAttributeNameList(toObjectClass)
    classRole = getClassRole(toObjectClass)
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
    args = []
    kwargs = fromJsonToDictionary.copy()
    # print(f'fromJsonToDictionary = {fromJsonToDictionary}')
    for key,value in fromJsonToDictionary.items() :
        try :
            toObjectClass(*args,**kwargs)
        except :
            newValue = kwargs.copy()[key]
            args.append(newValue)
            del kwargs[key]
        # print(f'args = {args}, kwargs = {kwargs}')
    objectInstance = toObjectClass(*args,**kwargs)
    if not objectInstance :
        raise Exception(f'Not possible to instanciate {toObjectClass.__name__} class in convertFromJsonToObject() method')
    return objectInstance
    # return toObjectClass(**fromJsonToDictionary)

@Method
def convertFromObjectToObject(fromObject,toObjectClass) :
    fromJson = json.loads(jsonifyIt(fromObject))
    # print(f'        fromJson = {fromJson}')
    return convertFromJsonToObject(fromJson,toObjectClass)
