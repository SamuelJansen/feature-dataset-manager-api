from FlaskHelper import Controller, ControllerMethod

@Controller(url = '/owners')
class OwnerController:

    @ControllerMethod()
    def get(self):
        return self.service.owner.findAll(), 200
