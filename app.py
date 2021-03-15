import globals
from python_framework import initialize
globalsInstance = globals.newGlobalsInstance(
    __file__
    , settingStatus = True
    , successStatus = True
    , errorStatus = True
    , debugStatus = True
    , failureStatus = False
    , warningStatus = False
    , wrapperStatus = False
    , testStatus = False
    , logStatus = False
    , printRootPathStatus = False
)

# from python_helper import log
# log.prettyPython(globals.newGlobalsInstance, 'settingsFileName', globalsInstance.settingsFileName, logLevel=log.DEBUG)
# log.prettyPython(globals.newGlobalsInstance, 'settingFilePath', globalsInstance.settingFilePath, logLevel=log.DEBUG)
# log.prettyPython(globals.newGlobalsInstance, 'settingTree', globalsInstance.settingTree, logLevel=log.DEBUG)
# log.prettyPython(globals.newGlobalsInstance, 'defaultSettingFileName', globalsInstance.defaultSettingFileName, logLevel=log.DEBUG)
# log.prettyPython(globals.newGlobalsInstance, 'defaultSettingFilePath', globalsInstance.defaultSettingFilePath, logLevel=log.DEBUG)
# log.prettyPython(globals.newGlobalsInstance, 'defaultSettingTree', globalsInstance.defaultSettingTree, logLevel=log.DEBUG)

import FeatureManager
app = FeatureManager.app
api = FeatureManager.api
jwt = FeatureManager.jwt

@initialize(api, defaultUrl = '/swagger', openInBrowser=False)
def runFlaskApplication(app):
    app.run(debug=True)

if __name__ == '__main__' :
    runFlaskApplication(app)
