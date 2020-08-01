from globals import Globals
globals = Globals(__file__,
    debugStatus = True,
    warningStatus = True,
    errorStatus = True,
    successStatus = True,
    failureStatus = True,
    settingStatus = True)
import FeatureManager, FlaskManager
app = FeatureManager.app
api = FeatureManager.api

@FlaskManager.initialize(defaultUrl = "/features")
def runFlaskApplication(app):
    app.run(debug=True)

if __name__ == '__main__' :
    runFlaskApplication(app)
