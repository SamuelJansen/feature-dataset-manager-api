from FlaskHelper import Validator, ValidatorMethod
import SkillDto, GlobalException, HttpStatus

@Validator()
class SkillValidator:

    @ValidatorMethod(requestClass=SkillDto.SkillPostRequestDto)
    def validadePostRequestDto(self,dto):
        ...

    @ValidatorMethod(requestClass=SkillDto.SkillRequestDto)
    def validadeRequestDto(self,dto):
        ...
