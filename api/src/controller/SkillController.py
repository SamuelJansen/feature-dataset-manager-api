from FlaskHelper import Controller, ControllerMethod
import SkillDto, SkillPostDto
import HttpStatus

@Controller(url = '/skills')
class SkillController:

    @ControllerMethod(requestClass = SkillPostDto.SkillPostDto)
    def post(self,dto):
        return self.service.skill.create(dto), HttpStatus.CREATED

    @ControllerMethod(url = '/<key>')
    def get(self, key=None):
        return self.service.skill.findByKey(key), HttpStatus.OK

    @ControllerMethod(url = '/<key>', requestClass = SkillDto.SkillDto)
    def put(self,dto,key):
        return self.service.skill.create(dto), HttpStatus.ACCEPTED

    @ControllerMethod(url = '/<key>')
    def delete(self,key):
        return self.service.skill.create(key), HttpStatus.NO_CONTENT

@Controller(url = '/skills/batch')
class SkillBatchController:

    @ControllerMethod()
    def get(self):
        return self.service.skill.findAll(), HttpStatus.OK
