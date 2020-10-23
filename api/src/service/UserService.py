from python_framework import Service, ServiceMethod
import User, UserDto

@Service()
class UserService:

    @ServiceMethod(requestClass=[UserDto.UserRequestDto, str])
    def create(self, dto, key):
        self.validator.user.postRequestDto(dto, key)
        model = self.mapper.user.fromPostRequestDtoToModel(dto, key)
        self.repository.user.save(model)
        return self.converter.user.fromModelToResponseDto(model)

    @ServiceMethod(requestClass=[UserDto.UserRequestDto, str])
    def update(self, dto, key):
        self.validator.user.putRequestDto(dto, key)
        model = self.findByKey(key)
        self.mapper.user.overrideModelValues(dto, model)
        self.repository.user.save(model)
        return self.converter.user.fromModelToResponseDto(model)

    @ServiceMethod(requestClass=str)
    def queryByKey(self, key):
        self.validator.common.strNotNull(key, 'key')
        model = self.findByKey(key)
        return self.converter.user.fromModelToResponseDto(model)

    @ServiceMethod()
    def queryAll(self):
        modelList = self.findAll()
        return self.converter.user.fromModelListToResponseDtoList(modelList)

    @ServiceMethod(requestClass=str)
    def delete(self, key):
        self.validator.user.existsByKey(key)
        self.repository.user.deleteByKey(key)

    @ServiceMethod(requestClass=str)
    def findByKey(self, key):
        self.validator.user.existsByKey(key)
        return self.repository.user.findByKey(key)

    @ServiceMethod()
    def findAll(self):
        return self.repository.user.findAll()

    @ServiceMethod(requestClass=str)
    def existsByKey(self, key):
        return self.repository.user.existsByKey(key)
