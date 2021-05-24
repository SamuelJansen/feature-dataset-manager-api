from python_helper import log
import globals
from python_framework import initialize, runApi
globalsInstance = globals.newGlobalsInstance(
    __file__
    , settingStatus = True
    , successStatus = True
    , errorStatus = True

    , debugStatus = True
    , warningStatus = False
    , wrapperStatus = False
    , failureStatus = False
    , testStatus = False
    , logStatus = False
    , printRootPathStatus = False
)
# try :
# log.prettyPython(globals.newGlobalsInstance, 'settingsFileName', globalsInstance.settingsFileName, logLevel=log.SETTING)
# log.prettyPython(globals.newGlobalsInstance, 'settingFilePath', globalsInstance.settingFilePath, logLevel=log.SETTING)
# log.prettyPython(globals.newGlobalsInstance, 'settingTree', globalsInstance.settingTree, logLevel=log.SETTING)
# log.prettyPython(globals.newGlobalsInstance, 'defaultSettingFileName', globalsInstance.defaultSettingFileName, logLevel=log.SETTING)
# log.prettyPython(globals.newGlobalsInstance, 'defaultSettingFilePath', globalsInstance.defaultSettingFilePath, logLevel=log.SETTING)
# log.prettyPython(globals.newGlobalsInstance, 'defaultSettingTree', globalsInstance.defaultSettingTree, logLevel=log.SETTING)

import FeatureManager
app = FeatureManager.app
api = FeatureManager.api
jwt = FeatureManager.jwt

@initialize(api, defaultUrl = '/swagger', openInBrowser=False)
def runFlaskApplication(app):
    runApi(debug=False, use_reloader=False)

if __name__ == '__main__' :
    runFlaskApplication(app)
# except Exception as exception :
#     log.error(log.error, 'Not possible to run', exception)

    # log.prettyPython(globals.newGlobalsInstance, 'settingsFileName', globalsInstance.settingsFileName, logLevel=log.SETTING)
    # log.prettyPython(globals.newGlobalsInstance, 'settingFilePath', globalsInstance.settingFilePath, logLevel=log.SETTING)
    # log.prettyPython(globals.newGlobalsInstance, 'settingTree', globalsInstance.settingTree, logLevel=log.SETTING)
    # log.prettyPython(globals.newGlobalsInstance, 'defaultSettingFileName', globalsInstance.defaultSettingFileName, logLevel=log.SETTING)
    # log.prettyPython(globals.newGlobalsInstance, 'defaultSettingFilePath', globalsInstance.defaultSettingFilePath, logLevel=log.SETTING)
    # log.prettyPython(globals.newGlobalsInstance, 'defaultSettingTree', globalsInstance.defaultSettingTree, logLevel=log.SETTING)
