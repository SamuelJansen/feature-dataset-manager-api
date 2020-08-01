from FlaskManager import Controller, ControllerMethod

@Controller(url = '/')
class HomeController:

    @ControllerMethod()
    def get(self):
        return {'status' : 'UP'}, 200
