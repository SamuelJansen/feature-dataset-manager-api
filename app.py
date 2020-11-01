from globals import Globals
from python_framework import initialize
globals = Globals(__file__,
    debugStatus = True,
    warningStatus = True,
    errorStatus = False,
    successStatus = True,
    failureStatus = True,
    settingStatus = True,
    printRootPathStatus = False)

import FeatureManager
app = FeatureManager.app
api = FeatureManager.api
jwt = FeatureManager.jwt

@initialize(api, defaultUrl = '/swagger', openInBrowser=False)
def runFlaskApplication(app):
    app.run(debug=True)

if __name__ == '__main__' :
    runFlaskApplication(app)
