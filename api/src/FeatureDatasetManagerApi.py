from python_framework import ResourceManager
import ModelAssociation

app = ResourceManager.initialize(
    __name__,
    ModelAssociation.Model
)

import os
from flask import send_from_directory

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )
