from python_helper import Constant
from OpenApiKey import Key

class Value:
    SWAGGER_VERSION = '2.0'
    URL = 'http://swagger.io/'
    EXTERNAL_DOCS = URL
    VERSION = '0.0.0'
    CONTACT_NAME = 'developer team'
    LICENSE_NAME = 'Not present'
    TAG_NAME = 'Tag Name'
    EMAIL = 'developer.team@email.com'
    HOST = '127.0.0.1:5000'
    BASE_PATH = '/'
    HTTPS = 'https'
    HTTP = 'http'
    SCHEMES = [HTTPS, HTTP]
    TITLE = Constant.NOTHING
    DESCRIPTION = Constant.NOTHING
    TYPE = Constant.NOTHING
    EXAMPLE = Constant.NOTHING
    SUMARY = Constant.NOTHING
    OPERATION_ID = Constant.NOTHING
    TERMS_OF_SERVICE = URL
    CONTACT = {
        Key.CONTACT_NAME : CONTACT_NAME,
        Key.EMAIL : EMAIL
    }
    INFO = {
        Key.TITLE : TITLE,
        Key.VERSION : VERSION,
        Key.DESCRIPTION : DESCRIPTION,
        Key.TERMS_OF_SERVICE : TERMS_OF_SERVICE,
        Key.CONTACT : CONTACT
    }
    LICENSE = {
        Key.LICENSE_NAME : LICENSE_NAME,
        Key.URL : URL
    }
    EXTERNAL_DOC = {
        Key.DESCRIPTION : DESCRIPTION,
        Key.URL : URL
    }
    TAG = {
        Key.TAG_NAME : TAG_NAME,
        Key.DESCRIPTION : DESCRIPTION,
        Key.EXTERNAL_DOCS : EXTERNAL_DOC
    }
    REQUIRED = []
    PROPERTIES = {}
    PROPERTY = {
        Key.TYPE : TYPE,
        Key.EXAMPLE : EXAMPLE
    }
    DEFINITIONS = {}
    DEFINITION = {
        Key.TYPE : TYPE,
        Key.REQUIRED : REQUIRED,
        Key.PROPERTIES : PROPERTIES
    }
    PATHS = {}
    PATH = {}
    TAGS = []
    CONSUMES = []
    PRODUCES = []
    PARAMETERS = []
    RESPONSES = {}
    SECURITY = {}
    VERB = {
        Key.TAGS : TAGS,
        Key.SUMARY : SUMARY,
        Key.DESCRIPTION : DESCRIPTION,
        Key.OPERATION_ID : OPERATION_ID,
        Key.CONSUMES : CONSUMES,
        Key.PRODUCES : PRODUCES,
        Key.PARAMETERS : PARAMETERS,
        Key.RESPONSES : RESPONSES,
        Key.SECURITY : SECURITY
    }
    VERBS = {}
    NEW = {}
    SWAGGER_DOC = {
        Key.SWAGGER_VERSION : SWAGGER_VERSION,
        Key.INFO : INFO,
        Key.HOST : HOST,
        Key.BASE_PATH : BASE_PATH,
        Key.TAGS : TAGS,
        Key.SCHEMES : SCHEMES,
        Key.PATHS : PATHS,
        Key.DEFINITIONS : DEFINITIONS
    }
