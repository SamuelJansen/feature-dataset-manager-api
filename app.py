import globals
from python_framework import initialize
globalsInstance = globals.newGlobalsInstance(
    __file__
    , settingStatus = True
    , successStatus = True
    , errorStatus = True
    , debugStatus = False
    , warningStatus = False
    , wrapperStatus = False
    , failureStatus = False
    , testStatus = False
    , logStatus = False
    , printRootPathStatus = True
)

import FeatureManager
app = FeatureManager.app
api = FeatureManager.api
jwt = FeatureManager.jwt

@initialize(api, defaultUrl = '/swagger', openInBrowser=False)
def runFlaskApplication(app):
    app.run(debug=True)

if __name__ == '__main__' :
    runFlaskApplication(app)
