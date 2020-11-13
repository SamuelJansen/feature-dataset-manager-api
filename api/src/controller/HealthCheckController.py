from python_framework import Controller, ControllerMethod, HttpStatus

@Controller(url='/actuator/health', tag='HealthCheck', description='HealthCheck controller')
class ActuatorHealthCheckController:

    @ControllerMethod()
    def get(self):
        return {'status' : 'UP'}, 200
