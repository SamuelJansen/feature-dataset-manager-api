from FlaskHelper import Controller, ControllerMethod
import SkillDto

@Controller(url = '/skills')
class SkillController:

    @ControllerMethod(url = '/<key>/<label>')
    def get(self, key=None, label=None):
        return self.service.skill.findByKey(key), 200

    @ControllerMethod(bodyRequestClass = SkillDto.SkillDto)
    def post(self,skillRequestDto):
        skillResponseDto = self.service.skill.create(skillRequestDto)
        if skillResponseDto :
            return skillResponseDto, 201
        else :
            return {'description' : 'Something bad happened. Please, try again later'}, 500

@Controller(url = '/skills/batch')
class SkillsController:

    @ControllerMethod()
    def get(self):
        return self.service.skill.findAll(), 200
