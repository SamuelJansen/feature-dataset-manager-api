from python_helper import log

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
            log.wraper(Method,f'''failed to execute{className}{methodName} method''',exception)
            raise Exception('Failed to return api from "globals" instance')
        return methodReturn
    return wrapedMethod
