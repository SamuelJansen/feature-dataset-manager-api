from python_helper import log, Constant

DOT_SPACE_CAUSE = f'{Constant.DOT_SPACE}{Constant.LOG_CAUSE}'

def Method(method,*args,**kwargs) :
    def wrapedMethod(*args,**kwargs) :
        try :
            methodReturn = method(*args,**kwargs)
        except Exception as exception :
            try :
                className = f' {args[0].__class__.__name__}'
            except :
                className = ''
            try :
                methodName = method.__name__
                if not className == '' :
                    methodName = f'.{methodName}'
                else :
                    methodName = f' {methodName}'
            except :
                methodName = ''
            log.wraper(Method,f'''failed to execute{className}{methodName} method. Received args: {args}. Received kwargs: {kwargs}''',exception)
            raise Exception(f'{className}{methodName} method error{DOT_SPACE_CAUSE}{str(exception)}')
        return methodReturn
    overrideSignatures(wrapedMethod, method)
    return wrapedMethod

def overrideSignatures(toOverride, original) :
    try :
        toOverride.__name__ = original.__name__
        toOverride.__module__ = original.__module__
        toOverride.__qualname__ = original.__qualname__
    except Exception as exception :
        log.wraper(overrideSignatures,f'''failed to override signatures of {toOverride} by signatures of {original} method''',exception)
