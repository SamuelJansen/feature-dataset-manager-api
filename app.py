from globals import Globals
globals = Globals(__file__,
    debugStatus = True,
    warningStatus = True,
    errorStatus = True,
    successStatus = True,
    failureStatus = True,
    settingStatus = True)
import SkillManager, FlaskHelper
app = SkillManager.app
api = SkillManager.api

@FlaskHelper.initialize(defaultUrl = "/skills")
def runFlaskApplication(app):
    app.run(debug=True)

if __name__ == '__main__' :
    runFlaskApplication(app)
