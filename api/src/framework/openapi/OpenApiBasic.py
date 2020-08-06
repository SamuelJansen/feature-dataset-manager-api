from python_helper import Constant, log
from OpenApiValue import Value
from OpenApiKeyValue import KeyValue

def new(**kwargs):
    return {**Value.NEW, **kwargs}

def newListByKey(key, *args, **kwargs):
    return {key : [*args]}

def newByKey(key, **kwargs):
    return {key : {**KeyValue.NEW[key], **new(**kwargs)}}

def newByHiddenKey(key, **kwargs):
    return {**KeyValue.NEW[key], **new(**kwargs)}

def newByKeyDict(key, newDict, **kwargs):
    new = newByHiddenKey(key, **kwargs)
    new.update(newDict)
    return {key : new}

def newByHiddenKeyDict(key, newDict, **kwargs):
    new = newByHiddenKey(key, **kwargs)
    new.update(newDict)
    return new

def newByKeyValue(key, value, **kwargs):
    return {value : newByKey(key, **kwargs)}

def newByHiddenKeyValue(key, value, **kwargs):
    return {value : newByHiddenKey(key, **kwargs)}
