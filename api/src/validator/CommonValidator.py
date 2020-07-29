from FlaskHelper import Validator, ValidatorMethod

@Validator()
class CommonValidator:

    @ValidatorMethod(requestClass=bool().__class__)
    def isBoolean(self, booleanObject):
        ...
