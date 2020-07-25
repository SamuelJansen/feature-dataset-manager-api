from FlaskHelper import Validator, ValidatorMethod
import SkillPostDto, GlobalException, HttpStatus

@Validator()
class SkillValidator:

    @ValidatorMethod(requestClass=SkillPostDto.SkillPostDto)
    def validadeSkillRequestDto(self,dto):
        ...
