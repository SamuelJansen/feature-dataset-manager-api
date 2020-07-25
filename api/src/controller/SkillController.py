from FlaskHelper import Controller, ControllerMethod
import SkillDto
import HttpStatus

@Controller(url = '/skills')
class SkillController:

    @ControllerMethod(requestClass = SkillDto.SkillPostRequestDto)
    def post(self,dto):
        return self.service.skill.create(dto), HttpStatus.CREATED

    @ControllerMethod(url = '/<key>')
    def get(self, key=None):
        return self.service.skill.findByKey(key), HttpStatus.OK

    @ControllerMethod(url = '/<key>', requestClass = SkillDto.SkillRequestDto)
    def put(self,dto,key):
        return self.service.skill.update(dto, key), HttpStatus.ACCEPTED

    @ControllerMethod(url = '/<key>')
    def delete(self,key):
        return self.service.skill.delete(key), HttpStatus.NO_CONTENT


@Controller(url = '/skills/batch')
class SkillBatchController:

    @ControllerMethod()
    def get(self):
        return self.service.skill.findAll(), HttpStatus.OK
