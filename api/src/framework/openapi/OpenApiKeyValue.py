from python_helper import Constant
from OpenApiKey import Key
from OpenApiValue import Value
from OpenApiKey import HiddenKey

class KeyValue:
    NEW = {
        Key.SWAGGER_VERSION : Value.SWAGGER_VERSION,
        Key.INFO : Value.INFO,
        Key.TITLE : Value.TITLE,
        Key.DESCRIPTION : Value.DESCRIPTION,
        Key.TERMS_OF_SERVICE : Value.TERMS_OF_SERVICE,
        Key.VERSION : Value.VERSION,
        Key.CONTACT : Value.CONTACT,
        Key.CONTACT_NAME : Value.CONTACT_NAME,
        Key.LICENSE_NAME : Value.LICENSE_NAME,
        Key.TAG_NAME : Value.TAG_NAME,
        Key.EMAIL : Value.EMAIL,
        Key.LICENSE : Value.LICENSE,
        Key.URL : Value.URL,
        Key.HOST : Value.HOST,
        Key.BASE_PATH : Value.BASE_PATH,
        Key.TAGS : Value.TAGS,
        Key.EXTERNAL_DOCS : Value.EXTERNAL_DOCS,
        Key.SCHEMES : Value.SCHEMES,
        Key.DEFINITIONS : Value.DEFINITIONS,
        Key.PROPERTIES : Value.PROPERTIES,
        Key.EXAMPLE : Value.EXAMPLE,
        Key.PROPERTY : Value.PROPERTY,
        Key.TYPE : Value.TYPE,
        Key.REQUIRED : Value.REQUIRED,
        Key.PATHS : Value.PATHS,
        Key.SUMARY : Value.SUMARY,
        Key.OPERATION_ID : Value.OPERATION_ID,
        Key.CONSUMES : Value.CONSUMES,
        Key.PRODUCES : Value.PRODUCES,
        Key.RESPONSES : Value.RESPONSES,
        Key.SECURITY : Value.SECURITY,
        Key.PARAMETERS : Value.PARAMETERS,

        HiddenKey.SWAGGER_DOC : Value.SWAGGER_DOC,
        HiddenKey.PATH : Value.PATH,
        HiddenKey.VERB : Value.VERB,
        HiddenKey.VERBS : Value.VERBS,
        HiddenKey.TAG : Value.TAG,
        HiddenKey.DEFINITION : Value.DEFINITION,
        HiddenKey.PROPERTY : Value.PROPERTY

    }
