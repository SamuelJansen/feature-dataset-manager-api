import globals
globalsInstance = globals.newGlobalsInstance(
    __file__
    , settingStatus = True
    , successStatus = True
    , errorStatus = True

    , debugStatus = False
    , warningStatus = False
    , wrapperStatus = False
    , failureStatus = True
    , testStatus = False
    , logStatus = False
    , infoStatus = False
    , printRootPathStatus = False
)

from python_framework import initialize, runApi
import FeatureManager
app = FeatureManager.app
api = FeatureManager.api
jwt = FeatureManager.jwt

@initialize(api, defaultUrl = '/swagger', openInBrowser=False)
def runFlaskApplication(app):
    runApi(debug=False, use_reloader=False)

if __name__ == '__main__' :
    runFlaskApplication(app)
