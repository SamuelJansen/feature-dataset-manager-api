from FlaskManager import Controller, ControllerMethod

@Controller(url='/health/check', tag='HealthCheck', description='HealthCheck controller')
class HealthCheckController:

    @ControllerMethod(url='/')
    def get(self):
        return {'status' : 'UP'}, 200

@Controller(url='/', tag='HealthCheck', description='HealthCheck controller')
class HealthCheckBatchController:

    @ControllerMethod(url='/')
    def get(self):
        return {'status' : 'UP'}, 200
