from python_framework import Controller, ControllerMethod, HttpStatus

@Controller(url='/actuator/health', tag='HealthCheck', description='HealthCheck controller')
class ActuatorHealthController:

    @ControllerMethod()
    def get(self):
        return {'status' : 'UP'}, HttpStatus.OK

@Controller(url='/', tag='HealthCheck', description='HealthCheck controller')
class ActuatorHealthBatchController:

    @ControllerMethod()
    def get(self):
        return {'status' : 'UP'}, HttpStatus.OK
