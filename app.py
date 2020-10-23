from globals import Globals
from python_framework import FlaskManager
globals = Globals(__file__,
    debugStatus = True,
    warningStatus = True,
    errorStatus = True,
    successStatus = True,
    failureStatus = True,
    settingStatus = True)
import FeatureManager
app = FeatureManager.app
api = FeatureManager.api
jwt = FeatureManager.jwt

@FlaskManager.initialize(defaultUrl = '/swagger', openInBrowser=True)
def runFlaskApplication(app):
    app.run(debug=True)

if __name__ == '__main__' :
    runFlaskApplication(app)
