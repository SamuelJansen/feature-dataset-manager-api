from werkzeug.security import safe_str_cmp
from python_framework import Validator, ValidatorMethod, Security, GlobalException, HttpStatus
import UserDto, User

@Validator()
class UserValidator:

    @ValidatorMethod(requestClass=User.User)
    def loggedUser(self,model):
        if not Security.getIdentity() == model.id :
            raise GlobalException.GlobalException(message="Unauthorized", status=HttpStatus.UNAUTHORIZED)

    @ValidatorMethod(requestClass=[UserDto.UserRequestDto, User.User])
    def password(self, dto, model):
        if not safe_str_cmp(model.password, dto.password) :
            raise GlobalException.GlobalException(message="Invalid username or password", status=HttpStatus.UNAUTHORIZED)

    @ValidatorMethod(requestClass=[UserDto.LoginRequestDto, str])
    def loginRequestDto(self, dto, key):
        self.existsByKey(key)
        self.validator.common.strNotNull(dto.password, 'password')
        self.validator.common.strNotNull(dto.email, 'email')

    @ValidatorMethod(requestClass=UserDto.UserRequestDto)
    def postRequestDto(self, dto, key):
        self.notExistsByKey(key)
        self.validator.common.strNotNull(dto.username, 'username')
        self.validator.common.strNotNull(dto.password, 'password')
        self.validator.common.strNotNull(dto.email, 'email')

    @ValidatorMethod(requestClass=[UserDto.UserRequestDto, str])
    def putRequestDto(self, dto, key):
        self.existsByKey(key)
        self.validator.common.strNotNull(dto.username, 'username')
        self.validator.common.strNotNull(dto.email, 'email')

    @ValidatorMethod(requestClass=str)
    def existsByKey(self, key):
        self.validator.common.strNotNull(key, 'key')
        if not self.service.user.existsByKey(key) :
            raise GlobalException.GlobalException(message=f'''User key does not exists''', status=HttpStatus.BAD_REQUEST)

    @ValidatorMethod(requestClass=str)
    def notExistsByKey(self, key):
        self.validator.common.strNotNull(key, 'key')
        if self.service.user.existsByKey(key) :
            raise GlobalException.GlobalException(message=f'''User key already exists''', status=HttpStatus.BAD_REQUEST)
