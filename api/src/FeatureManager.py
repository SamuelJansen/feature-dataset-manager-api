import os
import ResourceManager
import ModelAssociation

import os
print(os.environ['POSTGREE_CREDENTIALS'])

api, app, jwt = ResourceManager.initialize(
    __name__,
    ModelAssociation.Model,
    databaseEnvironmentVariable = 'POSTGREE_CREDENTIALS',
    jwtSecret = '3s7tj83ry17**q837yrk1v3r7k32vdg781dkd73u'
    # localStorageName = 'LocalFeatureManager'
)
