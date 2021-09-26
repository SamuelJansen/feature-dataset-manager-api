from werkzeug.security import safe_str_cmp
from python_framework import Validator, ValidatorMethod, Security, GlobalException, HttpStatus

from User import User
from dto.UserDto import LoginRequestDto, UserRequestDto

@Validator()
class UserValidator:

    @ValidatorMethod(requestClass=User)
    def loggedUser(self,model):
        if not Security.getIdentity() == model.id :
            raise GlobalException(message="Unauthorized", status=HttpStatus.UNAUTHORIZED)

    @ValidatorMethod(requestClass=[UserRequestDto, User])
    def password(self, dto, model):
        if not safe_str_cmp(model.password, dto.password) :
            raise GlobalException(message="Invalid username or password", status=HttpStatus.UNAUTHORIZED)

    @ValidatorMethod(requestClass=[LoginRequestDto, str])
    def loginRequestDto(self, dto, key):
        self.existsByKey(key)
        self.validator.common.strNotNull(dto.password, 'password')
        self.validator.common.strNotNull(dto.email, 'email')

    @ValidatorMethod(requestClass=UserRequestDto)
    def postRequestDto(self, dto, key):
        self.notExistsByKey(key)
        self.validator.common.strNotNull(dto.username, 'username')
        self.validator.common.strNotNull(dto.password, 'password')
        self.validator.common.strNotNull(dto.email, 'email')

    @ValidatorMethod(requestClass=[UserRequestDto, str])
    def putRequestDto(self, dto, key):
        self.existsByKey(key)
        self.validator.common.strNotNull(dto.username, 'username')
        self.validator.common.strNotNull(dto.email, 'email')

    @ValidatorMethod(requestClass=str)
    def existsByKey(self, key):
        self.validator.common.strNotNull(key, 'key')
        if not self.service.user.existsByKey(key) :
            raise GlobalException(message=f'''User key does not exists''', status=HttpStatus.BAD_REQUEST)

    @ValidatorMethod(requestClass=str)
    def notExistsByKey(self, key):
        self.validator.common.strNotNull(key, 'key')
        if self.service.user.existsByKey(key) :
            raise GlobalException(message=f'''User key already exists''', status=HttpStatus.BAD_REQUEST)
