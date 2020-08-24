import ResourceManager
import ModelAssociation

api, app, jwt = ResourceManager.initialize(
    __name__,
    ModelAssociation.Model,
    baseUrl = '/september',
    jwtSecret = '3s7tj83ry17**q837yrk1v3r7k32vdg781dkd73u',
    databaseEnvironmentVariable = 'DATABASE_URL'
    # localStorageName = 'LocalFeatureManager'
)
