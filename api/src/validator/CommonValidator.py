from python_helper import Constant
from python_framework import Validator, ValidatorMethod, GlobalException, HttpStatus

@Validator()
class CommonValidator:

    @ValidatorMethod(requestClass=bool)
    def isBoolean(self, booleanObject):
        ...

    @ValidatorMethod(requestClass=[str, str])
    def strNotNull(self, key, attributeName):
        if not key or Constant.NOTHING == key :
            raise GlobalException.GlobalException(message=f'''The atribute "{attributeName}" cannot be empty''', status=HttpStatus.BAD_REQUEST)

    @ValidatorMethod(requestClass=[str, str])
    def pathVariableNotNull(self, pathVariable, pathVariableName):
        if not pathVariable or Constant.NOTHING == pathVariable :
            raise GlobalException.GlobalException(message=f'''The path variable "{pathVariableName}" cannot be null''', status=HttpStatus.BAD_REQUEST)
