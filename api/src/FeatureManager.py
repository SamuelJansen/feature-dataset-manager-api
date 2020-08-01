import ResourceHelper
import ModelAssociation

api, app, jwt = ResourceHelper.initializeResources(
    __name__,
    ModelAssociation.Model,
    localStorageName = 'LocalFeatureManager',
    jwtSecret = '3s7tj83ry17**q837yrk1v3r7k32vdg781dkd73u'
)
