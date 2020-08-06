from FlaskManager import Controller, ControllerMethod

@Controller(url = '/health/check')
class HealthCheckController:

    @ControllerMethod()
    def get(self):
        return {'status' : 'UP'}, 200

@Controller(url = '/')
class HealthCheckBatchController:

    @ControllerMethod()
    def get(self):
        return {'status' : 'UP'}, 200
