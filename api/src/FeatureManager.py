import ResourceManager
import ModelAssociation

api, app, jwt = ResourceManager.initialize(
    __name__,
    ModelAssociation.Model,
    databaseEnvironmentVariable = 'DATABASE_URL',
    jwtSecret = '3s7tj83ry17**q837yrk1v3r7k32vdg781dkd73u'
    # localStorageName = 'LocalFeatureManager'
)
