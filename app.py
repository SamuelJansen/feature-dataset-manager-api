from python_framework import newApp, runApi
app = newApp(__file__,
    debugStatus = True
    , warningStatus = True
    , wrapperStatus = True
    , testStatus = True
    , logStatus = True
)
import globals
globalsInstance = globals.getGlobalsInstance()
print(globalsInstance.apiName)


print(type(app))
if __name__ == '__main__':
    runApi()
